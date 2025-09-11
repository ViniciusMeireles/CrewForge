from django.urls import reverse

from rest_framework.test import APIClient

from apps.accounts.models.member import Member


class CustomAPIClient(APIClient):
    def force_authenticate(self, user=None, token=None, member: Member = None, organization_auth: bool = True):
        """Force authentication of the user, token, or member."""
        if not member:
            super(CustomAPIClient, self).force_authenticate(user=user, token=token)
            return

        super(CustomAPIClient, self).force_authenticate(user=member.user, token=token)
        if organization_auth:
            self.post(
                path=reverse(viewname="accounts:organizations-login", args=[member.organization_id]),
                format="json",
            )
