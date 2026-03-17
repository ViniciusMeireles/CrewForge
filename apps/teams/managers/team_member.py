from apps.generics.managers.querysets import BaseManager, BaseQuerySet

TeamMemberManager = BaseManager.from_queryset(BaseQuerySet)
