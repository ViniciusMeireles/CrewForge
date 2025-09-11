from rest_framework import relations

from apps.generics.fields.fields import FieldMixin


class PrimaryKeyActiveRelatedFieldMixin:
    """
    Mixin to filter queryset based on the is_active field.
    """

    def get_queryset(self):
        """
        Override the get_queryset method to filter queryset based on the is_active field.
        This is useful for models that have an is_active field to filter out inactive records.
        """
        queryset = super().get_queryset()
        model = queryset.model
        filters = {"is_active": True} if hasattr(model, "is_active") else {}
        return queryset.filter(**filters)


class PrimaryKeyOrganizationRelatedFieldMixin(FieldMixin):
    """
    Mixin to filter queryset based on the organization_id field.
    """

    def get_queryset(self):
        """
        Override the get_queryset method to filter queryset based on the organization_id field.
        This is useful for models that have an organization_id field to filter records based on the organization.
        """
        queryset = super().get_queryset()
        model = queryset.model
        if hasattr(model, "organization_id"):
            filters = {"organization_id": self.auth_organization_id}
        else:
            filters = {}
        return queryset.filter(**filters)


class PrimaryKeyRelatedField(
    PrimaryKeyActiveRelatedFieldMixin,
    PrimaryKeyOrganizationRelatedFieldMixin,
    relations.PrimaryKeyRelatedField,
):
    """
    Custom field to handle the primary key related field in the serializer.
    This field is used to handle the primary key related field in the serializer.
    It combines the functionality of PrimaryKeyActiveRelatedFieldMixin and
    PrimaryKeyOrganizationRelatedFieldMixin to filter the queryset based on the is_active
    field and organization_id field.
    """
