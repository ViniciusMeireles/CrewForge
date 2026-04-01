# Architectural Patterns

This document describes the architectural patterns used in CrewForge.

---

## Table of Contents

- [Layered Architecture](#layered-architecture)
- [Facade Pattern](#facade-pattern)
- [Test Infrastructure](#test-infrastructure)

---

## Layered Architecture

CrewForge follows a strict layered architecture with clear separation of concerns.

### Layer Stack

```
┌─────────────────────────────────┐
│  Views / ViewSets               │  ← HTTP interface
├─────────────────────────────────┤
│  Permissions                    │  ← Access control
├─────────────────────────────────┤
│  Serializers                    │  ← Validation & serialization
├─────────────────────────────────┤
│  Filters                        │  ← Query filtering
├─────────────────────────────────┤
│  Models / Managers / QuerySets  │  ← Data layer
├─────────────────────────────────┤
│  Database (PostgreSQL)          │  ← Persistence
└─────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Location Pattern | Responsibility |
|-------|-----------------|----------------|
| Views | `apps/*/views/` | HTTP handling, routing, response formatting |
| Permissions | `apps/*/permissions/` | Access control, role-based authorization |
| Serializers | `apps/*/serializers/` | Input validation, output serialization |
| Filters | `apps/*/filters/` | Query parameter filtering via django-filter |
| Managers | `apps/*/managers/` | Custom query methods, bulk operations |
| Models | `apps/*/models/` | Domain entities, field definitions, relationships |

### Data Flow

A typical request flows through:

1. **URL Router** → dispatches to the correct ViewSet
2. **ViewSet** → applies `get_queryset()` with organization scoping
3. **Permission** → checks authentication, membership, and role
4. **Filter** → applies query parameter filters
5. **Serializer** → validates input or serializes output
6. **Model/Manager** → executes database operations

### ViewSet Composition

Standard viewset MRO follows a fixed order:

```python
class MyViewSet(
    OrganizationScopedViewSetMixin,    # 1st: scope by org
    ModelViewSetMixin,                  # 2nd: soft-delete + choices
    viewsets.ModelViewSet,              # 3rd: DRF base
):
    serializer_class = MySerializer
    queryset = MyModel.objects.all()
    permission_classes = [MyPermission]
    filterset_class = MyFilter
    label_expression = 'name'
```

---

## Facade Pattern

Facade patterns simplify complex operations by providing a unified interface over multiple subsystems.

### Schema Facade

Location: `apps/generics/utils/schema.py`

`extend_schema_model_view_set` provides a single decorator that configures all standard CRUD schema annotations for a ViewSet:

```python
def extend_schema_model_view_set(
    *,
    model: type[BaseModel],
    **kwargs,
):
    kwargs.setdefault('retrieve', extend_schema_retrieve(model=model))
    kwargs.setdefault('list', extend_schema_list(model=model))
    kwargs.setdefault('create', extend_schema_create(model=model))
    kwargs.setdefault('destroy', extend_schema_destroy(model=model))
    kwargs.setdefault('update', extend_schema_update(model=model))
    kwargs.setdefault('partial_update', extend_schema_partial_update(model=model))
    kwargs.setdefault('options', extend_schema_options(model=model))
    kwargs.setdefault('choices', extend_schema_choices_route(model=model))
    return extend_schema_view(**kwargs)
```

**Usage:**

```python
@extend_schema_model_view_set(model=Team)
class TeamViewSet(OrganizationScopedViewSetMixin, ModelViewSetMixin, viewsets.ModelViewSet):
    ...
```

This replaces 8 individual `@extend_schema` decorators with a single annotation.

### Request Helper Facade

Location: `apps/accounts/utils/requests.py`

Utility functions that encapsulate the multi-step process of extracting organization context from requests:

```python
def get_organization_id(request: Request) -> int | None:
    """Get the organization ID from the request."""
    if not request or not request.user.is_authenticated:
        return None
    return request.session.get('organization_id')


def get_organization(request: Request) -> Organization | None:
    """Get the organization from the request."""
    if not (organization_id := get_organization_id(request)):
        return None
    return request.user.organizations.filter(is_active=True).get_or_none(
        id=organization_id
    )


def get_member(request: Request) -> Member | None:
    """Get the member from the request."""
    if not request:
        return None
    user = request.user
    if not user.is_authenticated:
        return None
    if not (organization_id := request.session.get('organization_id')):
        return None
    return user.members.filter(is_active=True).get_or_none(
        organization_id=organization_id
    )


def is_same_organization_scope(
    obj,
    organization_id: int | None,
    lookup: str = 'organization_id',
    separator: str = '.',
) -> bool:
    """Check whether an object belongs to the given organization scope."""
    if not organization_id:
        return False
    current = obj
    for attr in lookup.split(separator):
        current = getattr(current, attr, None)
        if current is None:
            return False
    return current == organization_id
```

**Key features:**
- `get_organization_id()` — reads from session
- `get_organization()` — resolves the active org with `get_or_none()`
- `get_member()` — resolves the active member
- `is_same_organization_scope()` — supports dotted FK traversal via `separator`

### Serializer Context Facade

Location: `apps/generics/utils/serializers.py`

Encapsulates the logic for extracting an authenticated user from serializer context:

```python
def get_user_of_context(context: dict) -> User | None:
    request = context.get('request')
    if not request:
        return None
    elif not (user := request.user):
        return None
    elif not user.is_authenticated:
        return None
    if not user.is_active:
        return None
    return user
```

---

## Test Infrastructure

CrewForge provides shared test infrastructure for consistent API testing.

### CustomAPIClient

Location: `apps/accounts/tests/client.py`

Extends DRF's `APIClient` with organization-aware authentication:

```python
class CustomAPIClient(APIClient):
    def force_authenticate(
        self,
        user=None,
        token=None,
        member: MemberFactory | Member | None = None,
        organization_auth: bool = True,
    ):
        if not member:
            super(CustomAPIClient, self).force_authenticate(user=user, token=token)
            return

        super(CustomAPIClient, self).force_authenticate(user=member.user, token=token)
        if organization_auth:
            self.post(
                path=reverse(
                    viewname='accounts:organizations-login',
                    args=[member.organization_id],
                ),
                format='json',
            )
```

**Key behavior:** When authenticating with a `member`, it automatically performs the organization login step (step 3 of the auth flow), setting `organization_id` in the session.

### APITestCaseMixin

Location: `apps/accounts/tests/mixins.py`

Provides `new_account()` helper for creating organizations with authenticated owners:

```python
class APITestCaseMixin:
    client_class = CustomAPIClient
    client: CustomAPIClient = None

    def new_account(
        self, login: bool = True, organization_login: bool = True
    ) -> Organization:
        organization = OrganizationFactory.create()
        if login:
            if organization_login:
                self.client.force_authenticate(member=organization.owner)
            else:
                self.client.force_authenticate(user=organization.owner.user)
        return organization
```

**Parameters:**
- `login=True` — authenticate the user
- `organization_login=True` — also perform organization login (sets session context)

### Usage in Tests

```python
class TestMembersAPITestCase(APITestCaseMixin, APITestCase):
    def test_list_members(self):
        org = self.new_account()
        response = self.client.get('/api/accounts/members/')
        self.assertEqual(response.status_code, 200)

    def test_not_authenticated_list_members(self):
        response = self.client.get('/api/accounts/members/')
        self.assertEqual(response.status_code, 401)
```

---

## Related Patterns

- [Structural Patterns](./structural-patterns.md) (Mixin, Abstract Model, Module)
- [Behavioral Patterns](./behavioral-patterns.md) (Template Method, Strategy, Validation)
- [Creational Patterns](./creational-patterns.md) (Factory Method, Builder)
