from apps.generics.managers.querysets import BaseManager, BaseQuerySet


class InvitationQueryset(BaseQuerySet):
    pass


class InvitationManager(BaseManager.from_queryset(InvitationQueryset)):
    pass
