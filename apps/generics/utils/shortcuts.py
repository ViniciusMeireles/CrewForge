from django.db import models


def get_object_or_none(model_class: type[models.Model], **kwargs) -> models.Model | None:
    """Returns an object from the database based on past arguments."""
    try:
        return model_class.objects.get(**kwargs)
    except model_class.DoesNotExist:
        return None
