from django_filters.rest_framework import filterset

from apps.accounts.models.invitation import Invitation
from apps.generics.filters.mixins import FilterSetMixin


class InvitationFilter(FilterSetMixin, filterset.FilterSet):
    """Filter for the Invitation model."""

    class Meta:
        model = Invitation
        fields = {
            'email': ['exact', 'icontains'],
            'is_accepted': ['exact'],
            'is_expired': ['exact'],
            'expired_at': ['exact', 'gt', 'lt'],
            'role': ['exact', 'in'],
        }
