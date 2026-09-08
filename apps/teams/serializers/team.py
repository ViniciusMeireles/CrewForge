from django.db import transaction
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.mixins.serializers import ModelSerializerMixin
from apps.teams.choices import TeamMemberRoleChoices
from apps.teams.models.team import Team
from apps.teams.models.team_member import TeamMember


class TeamSerializer(ModelSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ModelSerializerMixin._default_read_only_fields + [
            'organization',
            'slug',
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs=attrs)
        errors = {}
        slug = attrs.get('slug') or slugify(attrs.get('name', ''))
        teams_queryset = Team.objects.filter(
            organization_id=self.auth_organization_id,
            slug=slug,
            is_active=True,
        )
        if self.instance:
            teams_queryset = teams_queryset.exclude(pk=self.instance.pk)
        if teams_queryset.exists():
            name_errors = errors.get('name', [])
            name_errors.append(_('This team already exists.'))
            errors['name'] = name_errors
        if errors:
            raise serializers.ValidationError(errors)
        attrs['slug'] = slug
        return attrs

    def create(self, validated_data):
        """Create a new team."""
        with transaction.atomic():
            instance = super().create(validated_data)
            TeamMember.objects.create(
                member=self.auth_member,
                team=instance,
                role=TeamMemberRoleChoices.OWNER,
                created_by=self.auth_user,
                updated_by=self.auth_user,
            )
        return instance


class TeamListSerializer(TeamSerializer):
    member_count = serializers.IntegerField(read_only=True)
