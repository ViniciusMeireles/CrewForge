from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from apps.accounts.choices import MemberRoleChoices
from apps.generics.utils.requests import get_member


class IsActiveMember(IsAuthenticated):
    """Custom permission to check if the user is an active member."""

    def has_permission(self, request, view):
        """Check if the user is an active member."""
        return super().has_permission(request, view) and (member := get_member(request)) and member.is_active

    def has_object_permission(self, request, view, obj):
        """Check if the user has object-level permission and is an active member."""
        return (
            super().has_object_permission(request, view, obj) and (member := get_member(request)) and member.is_active
        )


class MemberPermission(IsActiveMember):
    """Custom permission to check if the user has permission to perform actions on members."""

    def has_permission(self, request, view):
        if view.action == "create_with_invite":
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if (
            not super().has_object_permission(request, view, obj)
            or not (organization_id := request.session.get("organization_id"))
            or obj.organization_id != organization_id
        ):
            return False

        auth_member = get_member(request)
        if (
            request.method in permissions.SAFE_METHODS
            or (request.user.id == obj.user_id and obj.is_active)
            or (auth_member.has_admin_permission and request.method == "DELETE")
        ):
            return True

        auth_member = get_member(request)
        if auth_member != obj and request.method in ["PUT", "PATCH"]:
            return False

        return (obj.role == MemberRoleChoices.OWNER and auth_member.has_owner_permission) or (
            obj.role != MemberRoleChoices.OWNER and auth_member.has_admin_permission
        )
