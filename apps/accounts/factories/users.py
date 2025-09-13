from django.contrib.auth import get_user_model

import factory
from factory.django import DjangoModelFactory

User = get_user_model()
DEFAULT_PASSWORD = 'passWord*123'


class UserFactory(DjangoModelFactory):
    username = factory.Faker('user_name')
    email = factory.Sequence(lambda n: f'unit_test_user{n}@horologe.com')
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True

    class Meta:
        model = User
        skip_postgeneration_save = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.password = DEFAULT_PASSWORD
        if create:
            self.set_password(DEFAULT_PASSWORD)
            self.save()
