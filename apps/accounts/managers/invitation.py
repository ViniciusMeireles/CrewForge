from apps.generics.managers.querysets import BaseManager, BaseQuerySet

InvitationManager = BaseManager.from_queryset(BaseQuerySet)
