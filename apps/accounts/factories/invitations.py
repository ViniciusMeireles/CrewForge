from datetime import timezone

import factory
from factory.django import DjangoModelFactory

from apps.accounts.choices import MemberRoleChoices
from apps.accounts.models.invitation import Invitation
from apps.generics.factories.mixins import ModelFactoryMixin


class InvitationFactory(ModelFactoryMixin, DjangoModelFactory):
    email = factory.Sequence(lambda n: f'unit_test_invite{n}@horologe.com')
    is_accepted = False
    is_expired = False
    expired_at = factory.Faker('date_time', tzinfo=timezone.utc)
    role = MemberRoleChoices.MEMBER
    organization = factory.SubFactory(
        factory="apps.accounts.factories.organizations.OrganizationFactory",
    )

    class Meta:
        model = Invitation
        skip_postgeneration_save = True
