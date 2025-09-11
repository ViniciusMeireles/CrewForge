from django.urls import reverse

from rest_framework import status as http_status
from rest_framework.test import APITestCase

from apps.accounts.choices import MemberRoleChoices
from apps.accounts.factories.members import MemberFactory
from apps.accounts.factories.organizations import OrganizationFactory
from apps.accounts.factories.users import UserFactory


class SignupAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url_name = "accounts:signup-list"
        cls.url = reverse(cls.url_name)

    def test_create_account(self):
        """Test the create view of the signup."""
        user_data = UserFactory.build()
        organization_data = OrganizationFactory.build()
        member_data = MemberFactory.build()

        payload = {
            "user": {
                "username": user_data.username,
                "email": user_data.email,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "password": "passWord*123",
            },
            "organization": {
                "name": organization_data.name,
                "slug": organization_data.slug,
            },
            "nickname": member_data.nickname,
        }

        response = self.client.post(
            path=self.url,
            data=payload,
            format="json",
        )

        self.assertEqual(response.status_code, http_status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("user").get("username"), user_data.username)
        self.assertEqual(response.data.get("user").get("email"), user_data.email)
        self.assertEqual(response.data.get("user").get("first_name"), user_data.first_name)
        self.assertEqual(response.data.get("user").get("last_name"), user_data.last_name)
        self.assertEqual(response.data.get("organization").get("name"), organization_data.name)
        self.assertEqual(response.data.get("organization").get("slug"), organization_data.slug)
        self.assertEqual(response.data.get("nickname"), member_data.nickname)
        self.assertEqual(response.data.get("role"), MemberRoleChoices.OWNER)
        self.assertIsNotNone(response.data.get("access"))
        self.assertIsNotNone(response.data.get("refresh"))
