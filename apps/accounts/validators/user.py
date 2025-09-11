from django.contrib.auth import get_user_model
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

User = get_user_model()


@deconstructible
class UsernameExistValidator(BaseValidator):
    """Validator that checks if a username exists in the database."""

    message = _('User with this username does not exist.')

    def __init__(self, message=None):
        super().__init__(limit_value=None, message=message)

    def __call__(self, value):
        self.clean(value)

    def clean(self, value):
        if not User.objects.filter(username=value).exists():
            raise ValidationError(self.message)
        return value
