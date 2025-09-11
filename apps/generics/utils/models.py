from django.db import models


def get_verbose_name(model: type[models.Model]) -> str | None:
    """Get the verbose name of a model."""
    return model._meta.verbose_name if hasattr(model, '_meta') else str(model)


def get_verbose_name_plural(model: type[models.Model]) -> str | None:
    """Get the verbose name plural of a model."""
    return model._meta.verbose_name_plural if hasattr(model, '_meta') else get_verbose_name(model) + 's'


def get_verbose_name_field(model: type[models.Model], field_name: str) -> str:
    """Get the verbose name of a field in a model."""
    if hasattr(model, '_meta') and hasattr(model._meta, 'get_field'):
        try:
            return model._meta.get_field(field_name).verbose_name
        except Exception as e:
            return field_name
    return field_name
