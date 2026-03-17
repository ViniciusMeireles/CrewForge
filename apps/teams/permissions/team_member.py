from rest_framework import permissions

from apps.accounts.permissions.member import IsActiveMember
from apps.generics.utils.requests import get_member


class TeamMemberPermission(IsActiveMember):
    def has_object_permission(self, request, view, obj):
        if (
            not super().has_object_permission(request, view, obj)
            or not (organization_id := request.session.get('organization_id'))
            or obj.team.organization_id != organization_id
        ):
            return False

        auth_member = get_member(request)
        return request.method in permissions.SAFE_METHODS or (
            auth_member
            and (auth_member.id == obj.member_id or auth_member.has_manager_permission)
        )
