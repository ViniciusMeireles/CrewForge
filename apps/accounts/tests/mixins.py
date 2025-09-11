from apps.accounts.factories.organizations import OrganizationFactory
from apps.accounts.models.organization import Organization
from apps.accounts.tests.client import CustomAPIClient


class APITestCaseMixin:
    client_class = CustomAPIClient

    def new_account(self, login: bool = True, organization_login: bool = True) -> Organization:
        organization = OrganizationFactory.create()
        if login:
            if organization_login:
                self.client.force_authenticate(member=organization.owner)
            else:
                self.client.force_authenticate(user=organization.owner.user)
        return organization
