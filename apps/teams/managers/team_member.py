from apps.generics.managers.querysets import BaseManager, BaseQuerySet


class TeamMemberQueryset(BaseQuerySet):
    pass


class TeamMemberManager(BaseManager.from_queryset(TeamMemberQueryset)):
    pass
