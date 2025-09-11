from django.urls import reverse

from rest_framework import status as http_status
from rest_framework.test import APITestCase

from apps.accounts.choices import MemberRoleChoices
from apps.accounts.factories.members import MemberFactory
from apps.accounts.tests.mixins import APITestCaseMixin
from apps.teams.factories.teams import TeamFactory


class TeamAPITestCase(APITestCaseMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.detail_url_name = "teams:teams-detail"
        cls.list_url_name = "teams:teams-list"
        cls.list_url = reverse(cls.list_url_name)
        cls.choices_url = reverse("teams:teams-choices")

    def setUp(self):
        self.organization = self.new_account()

    def test_list_and_choices_teams(self):
        """Test the list and choices views of the teams."""
        TeamFactory.create_batch(size=8, organization=self.organization)

        for url in [self.list_url, self.choices_url]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, http_status.HTTP_200_OK)
            self.assertEqual(response.data.get("count"), 8)

    def test_create_team(self):
        """Test the create view of the teams."""

        team_data = TeamFactory.build()
        payload = {
            "name": team_data.name,
            "description": team_data.description,
            "slug": team_data.slug,
        }

        response = self.client.post(
            path=self.list_url,
            data=payload,
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), team_data.name)
        self.assertEqual(response.data.get("description"), team_data.description)
        self.assertEqual(response.data.get("slug"), team_data.slug)

    def test_retrieve_team(self):
        """Test the retrieve view of the teams."""
        team = TeamFactory(organization=self.organization)

        response = self.client.get(
            path=reverse(self.detail_url_name, args=[team.id]),
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), team.name)
        self.assertEqual(response.data.get("description"), team.description)
        self.assertEqual(response.data.get("slug"), team.slug)

    def test_update_team(self):
        """Test the update view of the teams."""
        team = TeamFactory(organization=self.organization)

        team_data = TeamFactory.build()
        payload = {
            "name": team_data.name,
            "description": team_data.description,
            "slug": team_data.slug,
        }

        response = self.client.put(
            path=reverse(self.detail_url_name, args=[team.id]),
            data=payload,
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), payload["name"])
        self.assertEqual(response.data.get("description"), payload["description"])
        self.assertEqual(response.data.get("slug"), payload["slug"])

    def test_delete_team(self):
        """Test the delete view of the teams."""
        team = TeamFactory(organization=self.organization)

        response = self.client.delete(
            path=reverse(self.detail_url_name, args=[team.id]),
        )
        self.assertEqual(response.status_code, http_status.HTTP_204_NO_CONTENT)

    def test_not_permission_team(self):
        """Test the delete view of the teams."""
        member = MemberFactory.create(
            organization=self.organization,
            role=MemberRoleChoices.MEMBER,
        )
        self.client.force_authenticate(member=member)

        team_data = TeamFactory.build()
        payload = {
            "name": team_data.name,
            "description": team_data.description,
            "slug": team_data.slug,
        }

        # Test create team
        response = self.client.post(
            path=self.list_url,
            data=payload,
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_403_FORBIDDEN)
