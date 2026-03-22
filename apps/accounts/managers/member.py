from apps.generics.managers.querysets import BaseManager, BaseQuerySet

MemberManager = BaseManager.from_queryset(BaseQuerySet)
