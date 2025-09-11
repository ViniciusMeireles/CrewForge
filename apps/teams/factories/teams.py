from django.utils.text import slugify

import factory
from factory.django import DjangoModelFactory

from apps.generics.factories.mixins import ModelFactoryMixin
from apps.teams.models.team import Team


class TeamFactory(ModelFactoryMixin, DjangoModelFactory):
    name = factory.Faker("company")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    description = factory.Faker("text", max_nb_chars=200)
    organization = factory.SubFactory(
        factory="apps.accounts.factories.organizations.OrganizationFactory",
    )

    class Meta:
        model = Team
