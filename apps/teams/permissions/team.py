from rest_framework import permissions

from apps.generics.utils.requests import get_member


class TeamPermission(permissions.BasePermission):
    """
    Custom permission to check if the user has permission to perform actions on teams.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.method in permissions.SAFE_METHODS or get_member(request).has_manager_permission
        )

    def has_object_permission(self, request, view, obj):
        if (
            not super().has_object_permission(request, view, obj)
            or not (organization_id := request.session.get("organization_id"))
            or obj.organization_id != organization_id
        ):
            return False
        elif request.method in permissions.SAFE_METHODS:
            return True

        auth_member = get_member(request)
        if auth_member.has_manager_permission:
            return True

        auth_member_team = auth_member.teams.filter(team_id=obj.id, is_active=True).get_or_none()
        return bool(auth_member_team) and auth_member_team.has_admin_permission
