from django.db import transaction

from rest_framework import serializers

from apps.accounts.choices import MemberRoleChoices
from apps.accounts.models.member import Member
from apps.accounts.models.organization import Organization
from apps.generics.serializers.mixins import ModelSerializerMixin


class OrganizationSerializer(ModelSerializerMixin, serializers.ModelSerializer):
    """Serializer for the Organization model."""

    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = ModelSerializerMixin._default_read_only_fields + ["owner"]

    def create(self, validated_data):
        """
        Override the create method to set the owner of the organization.
        """
        with transaction.atomic():
            instance = super().create(validated_data)
            member = Member.objects.create(
                user=self.auth_user,
                organization=instance,
                role=MemberRoleChoices.OWNER,
                created_by=self.auth_user,
                updated_by=self.auth_user,
            )
            instance.owner = member
            instance.save(update_fields=["owner"])
        return instance
