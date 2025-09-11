from django.contrib.auth.models import UserManager as BaseUserManager

from apps.generics.managers.querysets import BaseManager, BaseQuerySet


class UserQueryset(BaseQuerySet):
    pass


class UserManager(BaseManager.from_queryset(UserQueryset), BaseUserManager):
    pass
