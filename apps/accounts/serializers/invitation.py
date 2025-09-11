from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.accounts.models.invitation import Invitation
from apps.accounts.serializers.mixins import ValidateRoleSerializerMixin
from apps.generics.serializers.mixins import ModelSerializerMixin


class InvitationSerializer(ValidateRoleSerializerMixin, ModelSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = [
            "email",
            "is_expired",
            "is_accepted",
            "expired_at",
            "role",
            "organization",
        ]
        read_only_fields = ModelSerializerMixin._default_read_only_fields + [
            "key",
            "organization",
            "is_accepted",
        ]

    def validate_email(self, value):
        if value and not self.instance:
            invitation_queryset = Invitation.objects.filter(
                email=value,
                is_active=True,
                is_expired=False,
                is_accepted=False,
            ).exclude(
                expired_at__lt=timezone.now(),
            )
            if invitation_queryset.exists():
                raise serializers.ValidationError(_("An invitation with this email already exists."))
        return value

    def validate_organization(self, value):
        """Validate that the organization is not already associated with the member."""
        if value and self.instance and value != self.instance.organization:
            raise serializers.ValidationError(_("Not allowed to change the organization."))
        if not value and self.auth_organization:
            return self.auth_organization
        return value
