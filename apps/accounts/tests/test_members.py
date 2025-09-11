from django.urls import reverse
from django.utils import timezone

from rest_framework import status as http_status
from rest_framework.test import APITestCase

from apps.accounts.choices import MemberRoleChoices
from apps.accounts.factories.invitations import InvitationFactory
from apps.accounts.factories.members import MemberFactory
from apps.accounts.factories.users import UserFactory
from apps.accounts.tests.mixins import APITestCaseMixin


class MemberAPITestCase(APITestCaseMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.detail_url_name = "accounts:members-detail"
        cls.list_url_name = "accounts:members-list"
        cls.list_url = reverse(cls.list_url_name)
        cls.choices_url = reverse("accounts:members-choices")
        cls.create_with_invite_url_name = "accounts:members-create-with-invite"

    def setUp(self):
        self.organization = self.new_account()

    def _assert_data(self, response, user_data, member_data):
        """Helper method to assert the response data."""
        if user_data:
            self.assertEqual(response.data.get("user").get("username"), user_data.username)
            self.assertEqual(response.data.get("user").get("email"), user_data.email)
            self.assertEqual(response.data.get("user").get("first_name"), user_data.first_name)
            self.assertEqual(response.data.get("user").get("last_name"), user_data.last_name)
        if member_data:
            self.assertEqual(response.data.get("nickname"), member_data.nickname)
            self.assertEqual(response.data.get("role"), member_data.role)
            self.assertEqual(response.data.get("organization"), self.organization.id)

    @staticmethod
    def _payload_for_member(user_data, member_data):
        return {
            "user": {
                "username": user_data.username,
                "email": user_data.email,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "password": "passWord*123",
            },
            "nickname": member_data.nickname,
            "role": member_data.role,
        }

    def _create_member_with_invite(self, user_data, member_data):
        payload = self._payload_for_member(user_data=user_data, member_data=member_data)
        invite = InvitationFactory.create(
            organization=self.organization,
            email=user_data.email,
            role=member_data.role,
            expired_at=None,
        )
        return self.client.post(
            path=reverse(self.create_with_invite_url_name, args=[invite.key]),
            data=payload,
            format="json",
        )

    def test_list_and_choices_members(self):
        """Test the list and choices views of the members."""
        MemberFactory.create_batch(size=5, organization=self.organization)

        for url in [self.list_url, self.choices_url]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, http_status.HTTP_200_OK)
            self.assertEqual(response.data.get("count"), 6)

    def test_create_member_with_invite(self):
        """Test the create view of the members."""
        user_data = UserFactory.build()
        member_data = MemberFactory.build()

        response = self._create_member_with_invite(user_data, member_data)
        self.assertEqual(response.status_code, http_status.HTTP_201_CREATED)
        self._assert_data(response, user_data, member_data)
        self.assertIsNotNone(response.data.get("access"))
        self.assertIsNotNone(response.data.get("refresh"))

    def test_retrieve_member(self):
        """Test the retrieve view of the members."""
        member = MemberFactory(organization=self.organization)
        self.client.force_authenticate(member=member)

        response = self.client.get(
            path=reverse(self.detail_url_name, args=[member.id]),
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        self._assert_data(response, member.user, member)

    def test_update_member(self):
        """Test the update view of the members."""
        member = MemberFactory(organization=self.organization)
        self.client.force_authenticate(member=member)

        user_data = UserFactory.build()
        member_data = MemberFactory.build(role=member.role)
        payload = self._payload_for_member(user_data=user_data, member_data=member_data)
        payload.pop("role")

        response = self.client.put(
            path=reverse(self.detail_url_name, args=[member.id]),
            data=payload,
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        self._assert_data(response, user_data, member_data)

    def test_delete_member(self):
        """Test the delete view of the members."""
        member = MemberFactory(organization=self.organization)

        response = self.client.delete(
            path=reverse(self.detail_url_name, args=[member.id]),
        )
        self.assertEqual(response.status_code, http_status.HTTP_204_NO_CONTENT)

        # Verify that the member is deleted
        response = self.client.get(
            path=reverse(self.detail_url_name, args=[member.id]),
        )
        self.assertEqual(response.status_code, http_status.HTTP_404_NOT_FOUND)

    def test_not_permission_member(self):
        """Test the delete view of the members."""
        user_data = UserFactory.build()
        member_data = MemberFactory.build()
        payload = self._payload_for_member(user_data=user_data, member_data=member_data)

        # Test create member
        response = self.client.post(
            path=self.list_url,
            data=payload,
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test update member
        member = MemberFactory.create(
            organization=self.organization,
            role=MemberRoleChoices.MEMBER,
        )
        response = self.client.put(
            path=reverse(self.detail_url_name, args=[member.id]),
            data=payload,
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_403_FORBIDDEN)

        # Test delete member
        member_manager = MemberFactory.create(
            organization=self.organization,
            role=MemberRoleChoices.MANAGER,
        )
        self.client.force_authenticate(member=member_manager)
        response = self.client.delete(
            path=reverse(self.detail_url_name, args=[member.id]),
        )
        self.assertEqual(response.status_code, http_status.HTTP_403_FORBIDDEN)

        # Test retrieve member
        external_organization_member = MemberFactory.create()
        response = self.client.get(
            path=reverse(self.detail_url_name, args=[external_organization_member.id]),
        )
        self.assertEqual(response.status_code, http_status.HTTP_404_NOT_FOUND)

        inactive_member = MemberFactory.create(is_active=False)
        response = self.client.get(
            path=reverse(self.detail_url_name, args=[inactive_member.id]),
        )
        self.assertEqual(response.status_code, http_status.HTTP_404_NOT_FOUND)

    def test_duplicate_member(self):
        """Test the duplicate view of the members."""
        user_data = UserFactory.build()
        member_data = MemberFactory.build()

        # Create a member with the same email
        MemberFactory.create(
            organization=self.organization,
            user__email=user_data.email,
            role=member_data.role,
        )

        response = self._create_member_with_invite(user_data, member_data)
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

    def test_create_member_with_invite_expired(self):
        """Test the create member with invite when the invite is expired."""
        user_data = UserFactory.build()
        member_data = MemberFactory.build()

        # Create an expired invitation
        invite = InvitationFactory.create(
            organization=self.organization,
            email=user_data.email,
            role=member_data.role,
            expired_at=timezone.now() - timezone.timedelta(days=1),
            is_expired=True,
        )

        response = self.client.post(
            path=reverse(self.create_with_invite_url_name, args=[invite.key]),
            data=self._payload_for_member(user_data, member_data),
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_404_NOT_FOUND)
