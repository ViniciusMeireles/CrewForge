from rest_framework.permissions import IsAuthenticated

from apps.generics.utils.requests import (
    get_member,
    get_organization_id,
    is_same_organization_scope,
)


class IsActiveMember(IsAuthenticated):
    """Permission that requires an authenticated active member in session scope."""

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and (member := get_member(request))
            and member.is_active
        )

    def has_object_permission(self, request, view, obj):
        return (
            super().has_object_permission(request, view, obj)
            and (member := get_member(request))
            and member.is_active
        )


class OrganizationScopedPermission(IsActiveMember):
    """Base permission for objects that belong to the authenticated organization."""

    organization_lookup = 'organization_id'

    @classmethod
    def get_request_member(cls, request):
        return get_member(request)

    @classmethod
    def get_session_organization_id(cls, request):
        return get_organization_id(request)

    @classmethod
    def has_organization_scope(cls, request, obj) -> bool:
        organization_id = cls.get_session_organization_id(request)
        return is_same_organization_scope(
            obj=obj,
            organization_id=organization_id,
            lookup=cls.organization_lookup,
        )

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(
            request, view, obj
        ) and self.has_organization_scope(request, obj)
