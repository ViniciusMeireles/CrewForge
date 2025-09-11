from apps.generics.managers.querysets import BaseManager, BaseQuerySet


class MemberQueryset(BaseQuerySet):
    pass


class MemberManager(BaseManager.from_queryset(MemberQueryset)):
    pass
