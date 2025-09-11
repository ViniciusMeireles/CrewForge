from apps.generics.managers.querysets import BaseManager, BaseQuerySet


class OrganizationQueryset(BaseQuerySet):
    pass


class OrganizationManager(BaseManager.from_queryset(OrganizationQueryset)):
    pass


class OrganizationProfileQueryset(BaseQuerySet):
    pass


class OrganizationProfileManager(BaseManager.from_queryset(OrganizationProfileQueryset)):
    pass
