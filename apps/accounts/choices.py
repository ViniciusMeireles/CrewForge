from django.db import models
from django.utils.translation import gettext_lazy as _


class MemberRoleChoices(models.TextChoices):
    OWNER = 'owner', _('Owner')
    ADMIN = 'admin', _('Admin')
    MANAGER = 'manager', _('Manager')
    MEMBER = 'member', _('Member')
