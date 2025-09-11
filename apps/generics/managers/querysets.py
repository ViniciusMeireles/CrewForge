from django.db import models
from django.db.models import manager


class BaseQuerySet(models.QuerySet):
    def filter_actives(self):
        return self.filter(is_active=True)

    def filter_inactives(self):
        return self.filter(is_active=False)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class BaseManager(manager.BaseManager.from_queryset(BaseQuerySet)):
    def deactivate(self):
        return self.filter_actives().update(is_active=False)

    def activate(self):
        return self.filter_inactives().update(is_active=True)
