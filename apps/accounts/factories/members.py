import factory
from factory.django import DjangoModelFactory

from apps.accounts.choices import MemberRoleChoices
from apps.accounts.factories.users import UserFactory
from apps.accounts.models.member import Member
from apps.generics.factories.mixins import ModelFactoryMixin


class MemberFactory(ModelFactoryMixin, DjangoModelFactory):
    """Factory for creating Member instances."""

    nickname = factory.Faker('user_name')
    user = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(
        factory="apps.accounts.factories.organizations.OrganizationFactory",
    )
    role = MemberRoleChoices.MEMBER

    class Meta:
        model = Member
