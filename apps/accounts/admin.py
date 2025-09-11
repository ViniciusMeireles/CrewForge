from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.accounts.models.invitation import Invitation
from apps.accounts.models.member import Member
from apps.accounts.models.organization import Organization

admin.site.register(get_user_model())
admin.site.register(Organization)
admin.site.register(Member)
admin.site.register(Invitation)
