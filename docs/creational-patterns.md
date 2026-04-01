# Creational Design Patterns

This document describes the creational design patterns used in CrewForge.

---

## Table of Contents

- [Factory Method Pattern](#factory-method-pattern)
- [Builder Pattern](#builder-pattern)

---

## Factory Method Pattern

CrewForge uses [factory_boy](https://factoryboy.readthedocs.io/) with a custom mixin to provide consistent test data generation.

### ModelFactoryMixin

Location: `apps/generics/factories/mixins.py`

Base mixin applied to all factories, ensuring every model instance has `is_active = True` and a generated `id`.

```python
class ModelFactoryMixin:
    id = factory.Faker('id')
    is_active = True
```

### Factory Convention

All factories follow these rules:

1. Extend both `ModelFactoryMixin` and `DjangoModelFactory`
2. Use `factory.SubFactory` for ForeignKey relationships
3. Use `factory.LazyAttribute` for derived fields (e.g., `slug` from `name`)
4. Use `factory.post_generation` for related object creation when needed

### OrganizationFactory

Location: `apps/accounts/factories/organizations.py`

```python
class OrganizationFactory(ModelFactoryMixin, DjangoModelFactory):
    name = factory.Faker('company')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))

    class Meta:
        model = Organization
        skip_postgeneration_save = True

    @factory.post_generation
    def owner(self, create, extracted, **kwargs):
        if not create:
            return
        from apps.accounts.factories.members import MemberFactory
        from apps.accounts.factories.users import UserFactory
        owner_user = UserFactory()
        self.owner = MemberFactory(
            user=owner_user,
            organization=self,
            role=MemberRoleChoices.OWNER.value,
        )
        self.save()
```

### MemberFactory

Location: `apps/accounts/factories/members.py`

```python
class MemberFactory(ModelFactoryMixin, DjangoModelFactory):
    nickname = factory.Faker('user_name')
    user = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(
        factory='apps.accounts.factories.organizations.OrganizationFactory',
    )
    role = MemberRoleChoices.MEMBER

    class Meta:
        model = Member
```

### TeamFactory

Location: `apps/teams/factories/teams.py`

```python
class TeamFactory(ModelFactoryMixin, DjangoModelFactory):
    name = factory.Faker('company')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    description = factory.Faker('text', max_nb_chars=200)
    organization = factory.SubFactory(
        factory='apps.accounts.factories.organizations.OrganizationFactory',
    )

    class Meta:
        model = Team
```

### Factory Usage in Tests

```python
# Create with DB persistence
org = OrganizationFactory.create()
member = MemberFactory.create(organization=org)

# Build without DB persistence
team = TeamFactory.build()

# Batch creation
members = MemberFactory.create_batch(5, organization=org)
```

---

## Builder Pattern

The Builder pattern constructs complex objects step by step. CrewForge uses this for email composition.

### EmailBase as Builder

Location: `apps/generics/mails/bases.py`

`EmailBase` acts as a builder for `EmailMultiAlternatives` messages. Configuration happens through attributes and constructor kwargs, then `get_message()` builds the final object.

```python
# Step 1: Configure via subclass attributes
class PasswordResetRequestEmail(EmailBase):
    subject = _('Password Reset')
    preheader = _('Use the link below to reset your password.')
    title = _('Password Reset Request')
    content = _('Click the button below to set a new password.')

# Step 2: Build with constructor kwargs
email = PasswordResetRequestEmail(
    recipient_list=['user@example.com'],
    reset_url='https://app.example.com/reset?token=abc123',
)

# Step 3: Get the built message
message = email.get_message()

# Step 4: Send
email.send()
```

### CTAEmail

Location: `apps/generics/mails/bases.py`

Helper builder for Call-To-Action buttons within emails:

```python
class CTAEmail:
    def __init__(
        self,
        *,
        url: str,
        text: str = _('Click Here'),
        color: str = '#002180',
        text_color: str = '#FFFFFF',
    ):
        self.url = url
        self.text = text
        self.color = color
        self.text_color = text_color
```

**Usage:**

```python
self.cta = CTAEmail(
    url=reset_url,
    text=_('Reset Password'),
    color='#FF5733',
)
```

### EmailView for Preview

`EmailView` provides a Django view that builds the email in preview mode for development:

```python
# Only available in local/test environments
if settings.ENVIRONMENT in ['local_development', 'test']:
    urlpatterns += [
        path(
            route='email-preview/auth/password/reset/',
            view=PasswordResetRequestEmail.as_view(),
            name='password_reset_email_preview',
        )
    ]
```

---

## Related Patterns

- [Structural Patterns](./structural-patterns.md) (Mixin, Abstract Model, Module)
- [Behavioral Patterns](./behavioral-patterns.md) (Template Method, Strategy, Validation)
- [Architectural Patterns](./architectural-patterns.md) (Layered, Facade, Test Infrastructure)
