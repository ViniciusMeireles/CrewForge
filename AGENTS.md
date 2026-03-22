# AGENTS.md

## Purpose

This repository contains **CrewForge**, a Django REST API for managing:

- organizations
- members
- invitations
- teams
- team memberships
- authentication and password reset

The project centers on **organization-aware access control**. Beyond JWT auth,
users can set an active organization context through
`/api/accounts/organizations/{id}/login/`, which stores `organization_id` in the
session. Many queries, permissions, and tests depend on that behavior.


## Authentication Flow

User login in this project must be understood as a 3-step process:

1. Authenticate the user with `POST /api/auth/token/`
2. List the organizations available to that authenticated user with
   `GET /api/accounts/organizations/`
3. Select the active organization context with
   `POST /api/accounts/organizations/{id}/login/`

Important: step 1 authenticates the user, but it does not fully establish the
organization context required by several organization-scoped endpoints. Agents
must not assume that obtaining a JWT alone is enough to represent a fully logged
in user in CrewForge.


## Stack And Runtime

- Python `>=3.14`
- Django
- Django REST Framework
- `django-filter`
- `djangorestframework-simplejwt`
- `drf-spectacular` + sidecar assets
- PostgreSQL
- `uv` for dependency and command execution
- Docker / Docker Compose
- Gunicorn
- Ruff for linting and formatting
- pytest + pytest-django + factory-boy for tests

If the local machine does not match the required Python version or Postgres
setup, prefer the Docker workflow.


## Repository Map

- `config/`
  - project settings, URL config, WSGI/ASGI entrypoints
- `apps/accounts/`
  - organizations, members, invitations, signup, JWT customization, password reset
- `apps/teams/`
  - teams and team memberships
- `apps/generics/`
  - shared mixins, schema helpers, serializer helpers, filters, permissions, abstract models
- `templates/`
  - shared templates and email templates
- `static/`
  - static assets
- `schema.yml`
  - generated OpenAPI schema


## Development Modes

### Docker-first workflow

Primary services in `docker-compose.yml`:

- `postgres_db`
- `django_api`

Common commands:

- `make build`
- `make up`
- `make down`
- `make logs`
- `make migrate`
- `make createsuperuser`
- `make shell_plus`
- `make spectacular`
- `make format_code`
- `make test`
- `make precommit`

### Local uv workflow

Local equivalents are available through the `l_*` Make targets:

- `make l_migrate`
- `make l_spectacular`
- `make l_format_code`
- `make l_test`

Important: local tests use `test.env`, and `test.env` points Postgres to
`localhost:5432`. Make sure a compatible local Postgres instance is running.


## Environment Notes

- Copy `example.env` to `.env` for local Docker development.
- The example development setup uses `DJANGO_SETTINGS_MODULE=config.settings.local`.
- Base settings are production-leaning:
  - `DEBUG = False`
  - secure cookies enabled
  - HSTS enabled
  - SSL redirect enabled
- `config.settings.local` explicitly relaxes those settings for development.
- `run.sh` runs migrations and `collectstatic` before starting the app.
- In production mode the app runs with Gunicorn on port `8000`.
- In local/dev mode the container runs Django `runserver` on port `8000`.


## API And Domain Conventions

- Accounts endpoints live under `/api/accounts/`.
- Team endpoints live under `/api/teams/`.
- Auth endpoints live under `/api/auth/`.
- Root `/` redirects to Swagger UI at `/api/schema/swagger-ui/`.
- Treat login as a 3-step flow:
  - `POST /api/auth/token/`
  - `GET /api/accounts/organizations/`
  - `POST /api/accounts/organizations/{id}/login/`
- Role hierarchy from the README:
  - Owner
  - Admin
  - Manager
  - Member

Preserve this domain model when adding or changing behavior. Permission changes
should be treated as high impact and accompanied by tests.


## Code Organization Rules

- Put organization, membership, invitation, and auth logic in `apps/accounts/`.
- Put team and team membership logic in `apps/teams/`.
- Put reusable cross-app code in `apps/generics/`.
- Avoid duplicating shared helpers in feature apps when a generic helper belongs
  in `apps/generics/`.

When adding a new API resource, align with the existing structure:

- model
- manager/queryset if needed
- serializer
- filter
- permission
- viewset
- router registration
- tests


## Existing Patterns To Reuse

### Viewsets

Prefer existing shared mixins before creating new behavior:

- `apps.generics.views.mixins.ModelViewSetMixin`
  - adds the `choices` action
  - soft-deletes via `inactivate()` when a model has `is_active`
- `apps.generics.views.mixins.OrganizationScopedViewSetMixin`
  - scopes querysets by the authenticated organization context

### Schema

Keep API documentation consistent by reusing:

- `apps.generics.utils.schema.extend_schema_model_view_set`
- `apps.generics.utils.schema.extend_schema_choices_route`

If an endpoint changes request/response behavior, update the schema annotations
and regenerate `schema.yml`.

### Filtering

The default DRF filter backend is `django_filters.rest_framework.DjangoFilterBackend`.
Prefer explicit filter classes in each app instead of ad-hoc query parsing.

### i18n

User-facing strings and schema descriptions commonly use `gettext_lazy`.
Follow that pattern for new API messages and schema text.


## Style And Formatting

Ruff configuration in `pyproject.toml` is the source of truth:

- line length: `88`
- indent width: `4`
- target version: `py314`
- quote style: `single`
- lint rules selected: `E`, `F`, `I`, `B`, `W`

Ruff excludes migrations, caches, virtualenvs, and `__init__.py` files in the
configured paths. Even so, keep those files clean and minimal.


## Testing Guidance

- Test framework: `pytest` / `pytest-django`
- API tests currently use DRF `APITestCase` heavily
- Prefer `factory-boy` factories over manual object creation
- Test files live under `apps/*/tests/`

Important project-specific testing pattern:

- `apps.accounts.tests.client.CustomAPIClient.force_authenticate(member=...)`
  authenticates the underlying user and also performs organization login
- `apps.accounts.tests.mixins.APITestCaseMixin.new_account()` creates an
  organization and can auto-login the owner

Use these helpers whenever the behavior under test depends on
`request.session['organization_id']`.


## Required Checks Before Finishing

Run the relevant checks for the change you made:

- `make l_format_code`
- `make l_test`
- `make l_spectacular` if you changed endpoints, serializers, filters, examples, or schema annotations

If models change, create and review migrations as part of the same change.


## Practical Guardrails For Agents

- Do not replace the organization-context login flow with JWT-only assumptions.
- Do not switch the project to SQLite; configuration and tests are built around PostgreSQL.
- Do not bypass existing permission classes when adding new actions.
- Keep Swagger/ReDoc behavior working from `config/urls.py`.
- Keep README-visible behavior and generated schema aligned when the API surface changes.


## Definition Of Done

A change is usually ready when:

- code follows the existing app boundaries
- permissions and organization scoping are preserved
- tests cover the new behavior or regression
- Ruff passes
- OpenAPI schema is regenerated when API contracts changed
