from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers

from apps.generics.models.abstracts import BaseModel
from apps.generics.utils.models import get_verbose_name, get_verbose_name_plural


def extend_schema_choices_route(
    *,
    model: type[BaseModel],
    **kwargs,
):
    """
    Extend schema for choices route.
    This function is used to extend the schema for a choices route in the API.
    """
    description = _(
        "List %(name_plural)s for choices (value/label format)."
        % {"name_plural": model._meta.verbose_name_plural.lower()}
    )
    default_kwargs = {
        "tags": model.schema_tags(),
        "description": description,
        "responses": {
            200: OpenApiResponse(
                response=inline_serializer(
                    name=f"{model.__name__}ChoicesResponse",
                    fields={
                        "value": serializers.IntegerField(),
                        "label": serializers.CharField(),
                    },
                    many=True,
                ),
                examples=[
                    OpenApiExample(
                        name=_('Example response'),
                        value=[
                            {"value": 1, "label": f"{get_verbose_name(model).capitalize()} 1"},
                            {"value": 2, "label": f"{get_verbose_name(model).capitalize()} 2"},
                        ],
                        response_only=True,
                    )
                ],
                description=description,
            )
        },
    }
    default_kwargs.update(kwargs)
    return extend_schema(**default_kwargs)


def extend_schema_model_view_set(
    *,
    model: type[BaseModel],
    **kwargs,
):
    tags = kwargs.pop("tags", model.schema_tags())
    default_kwargs = {
        "retrieve": extend_schema(
            tags=tags,
            description=_("Retrieve a specific %(name)s." % {"name": get_verbose_name(model)}),
        ),
        "list": extend_schema(
            tags=tags,
            description=_("List all %(name)s." % {"name": get_verbose_name_plural(model)}),
        ),
        "create": extend_schema(
            tags=tags,
            description=_("Create a new %(name)s." % {"name": get_verbose_name(model)}),
        ),
        "destroy": extend_schema(
            tags=tags,
            description=_("Delete a %(name)s." % {"name": get_verbose_name(model)}),
        ),
        "update": extend_schema(
            tags=tags,
            description=_("Update a %(name)s." % {"name": get_verbose_name(model)}),
        ),
        "options": extend_schema(
            tags=tags,
            description=_("Get %(name)s options." % {"name": get_verbose_name(model)}),
        ),
        "choices": extend_schema_choices_route(model=model, tags=tags),
    }
    default_kwargs.update(kwargs)
    return extend_schema_view(**default_kwargs)
