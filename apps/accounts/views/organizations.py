from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import backends
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.filters.organization import OrganizationFilter
from apps.accounts.models.organization import Organization
from apps.accounts.permissions.organization import OrganizationPermission
from apps.accounts.serializers.organization import OrganizationSerializer
from apps.generics.utils.schema import extend_schema_model_view_set
from apps.generics.views.mixins import ModelViewSetMixin


@extend_schema_model_view_set(
    model=Organization,
    login=extend_schema(
        tags=Organization.schema_tags(),
        description=_("Login to the organization."),
        request=None,
        responses={
            http_status.HTTP_200_OK: OpenApiResponse(
                response=inline_serializer(
                    name="LoginResponse",
                    fields={
                        "detail": serializers.CharField(),
                    },
                ),
                examples=[
                    OpenApiExample(
                        name=_("Login to organization"),
                        value={"detail": _("Logged in to organization.")},
                        response_only=True,
                    )
                ],
                description=_("Logged in to organization."),
            ),
            http_status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=inline_serializer(
                    name="LoginNotFoundResponse",
                    fields={
                        "detail": serializers.CharField(),
                    },
                ),
                examples=[
                    OpenApiExample(
                        name=_("Organization not found"),
                        value={"detail": _("Organization not found.")},
                        response_only=True,
                    )
                ],
                description=_("Organization not found."),
            ),
        },
    ),
)
class OrganizationViewSet(ModelViewSetMixin, viewsets.ModelViewSet):
    """View for handling organization CRUD operations."""

    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    http_method_names = ["get", "put", "post", "delete", "options"]
    permission_classes = [OrganizationPermission]
    filterset_class = OrganizationFilter
    filter_backends = [backends.DjangoFilterBackend]
    label_expression = "name"

    def get_queryset(self):
        """Override the get_queryset method to filter organizations by the authenticated user."""
        queryset = super().get_queryset()
        if self.action == 'login':
            return queryset.filter(
                members__user_id=self.auth_user.id,
                members__is_active=True,
                is_active=True,
            )
        return queryset

    @action(detail=True, methods=["post"])
    def login(self, request, *args, **kwargs):
        """Login to the organization."""
        if not (organization := self.get_object()):
            return Response(
                data={"detail": _("Organization not found.")},
                status=http_status.HTTP_404_NOT_FOUND,
            )

        # Set the organization in the session
        request.session["organization_id"] = organization.id
        return Response(
            data={"detail": _("Logged in to organization.")},
            status=http_status.HTTP_200_OK,
        )
