from apps.generics.managers.querysets import BaseManager, BaseQuerySet

OrganizationManager = BaseManager.from_queryset(BaseQuerySet)
OrganizationProfileManager = BaseManager.from_queryset(BaseQuerySet)
