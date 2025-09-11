from django.contrib import admin

from apps.teams.models.team import Team
from apps.teams.models.team_member import TeamMember

admin.site.register(Team)
admin.site.register(TeamMember)
