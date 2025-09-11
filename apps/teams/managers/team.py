from apps.generics.managers.querysets import BaseManager, BaseQuerySet


class TeamQueryset(BaseQuerySet):
    pass


class TeamManager(BaseManager.from_queryset(TeamQueryset)):
    pass
