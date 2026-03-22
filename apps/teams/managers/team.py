from apps.generics.managers.querysets import BaseManager, BaseQuerySet

TeamManager = BaseManager.from_queryset(BaseQuerySet)
