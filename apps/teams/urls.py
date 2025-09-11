from django.urls import include, path

from rest_framework import routers

from apps.teams.views.team_members import TeamMemberViewSet
from apps.teams.views.teams import TeamViewSet

app_name = "teams"


router = routers.DefaultRouter()
router.register(r"teams", TeamViewSet, basename="teams")
router.register(r"team-members", TeamMemberViewSet, basename="team_members")


urlpatterns = [
    path('api/teams/', include(router.urls)),
]
