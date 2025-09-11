from django_filters.rest_framework import backends
from rest_framework import viewsets

from apps.generics.utils.schema import extend_schema_model_view_set
from apps.generics.views.mixins import ModelViewSetMixin
from apps.teams.filters.team import TeamFilter
from apps.teams.models.team import Team
from apps.teams.permissions.team import TeamPermission
from apps.teams.serializers.team import TeamSerializer


@extend_schema_model_view_set(model=Team)
class TeamViewSet(ModelViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    http_method_names = ["get", "post", "put", "delete", "options"]
    permission_classes = [TeamPermission]
    filterset_class = TeamFilter
    filter_backends = [backends.DjangoFilterBackend]
    label_expression = "name"

    def get_queryset(self):
        """Get the queryset for the view."""
        return super().get_queryset().filter(organization_id=self.auth_organization_id)
