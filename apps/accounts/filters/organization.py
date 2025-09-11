from django_filters.rest_framework import filterset

from apps.accounts.models.organization import Organization
from apps.generics.filters.mixins import FilterSetMixin


class OrganizationFilter(FilterSetMixin, filterset.FilterSet):
    """Filter for the Organization model."""

    class Meta:
        model = Organization
        fields = {
            'name': ['exact', 'icontains'],
            'slug': ['exact', 'icontains'],
            'is_active': ['exact'],
        }
