from django.contrib.auth import get_user_model
from django.utils.functional import cached_property

from apps.accounts.models.member import Member
from apps.accounts.models.organization import Organization
from apps.generics.utils.requests import get_member, get_organization, get_organization_id
from apps.generics.utils.serializers import get_user_of_context

User = get_user_model()


class FieldMixin:
    @cached_property
    def auth_user(self) -> User | None:
        """Get the user from the context."""
        return get_user_of_context(self.context)

    @cached_property
    def auth_member(self) -> Member | None:
        """Get the member from the context."""
        return get_member(self.context.get("request"))

    @cached_property
    def auth_organization(self) -> Organization | None:
        """Get the organization from the context."""
        return get_organization(self.context.get("request"))

    @cached_property
    def auth_organization_id(self) -> int | None:
        """Get the organization ID from the context."""
        return get_organization_id(self.context.get("request"))
