from django.conf import settings
from django.utils.translation import gettext as _

from apps.generics.mails.bases import CTAEmail, EmailBase


class PasswordResetRequestEmail(EmailBase):
    template_name = 'accounts/emails/base.html'

    subject = _('Password Reset')
    preheader = _('Use the link below to reset your password.')
    title = _('Password Reset Request')
    content = _(
        'We received a request to reset your password. Click the button below to set a new password. '
        'If you did not request this, please ignore this email.'
    )

    def __init__(self, *, reset_url: str, **kwargs):
        super().__init__(**kwargs)
        self.cta = CTAEmail(url=reset_url, text=_('Reset Password'))

    @classmethod
    def get_preview_kwargs(cls, **kwargs) -> dict:
        kwargs = super().get_preview_kwargs(**kwargs)
        kwargs.update(
            {
                'reset_url': f'{settings.FRONTEND_RESET_URL}?uid=abc123&token=def456',
            }
        )
        return kwargs
