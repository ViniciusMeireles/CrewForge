from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.generics.models.abstracts import BaseModel
from apps.teams.managers.team import TeamManager


class Team(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_("Name"), help_text=_("Name of the team"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"), help_text=_("Team slug"))
    description = models.TextField(
        null=True, blank=True, verbose_name=_("Description"), help_text=_("Description of the team")
    )
    organization = models.ForeignKey(
        to="accounts.Organization",
        on_delete=models.CASCADE,
        related_name='teams',
        verbose_name=_("Organization"),
        help_text=_("Organization to which the team belongs"),
    )

    objects = TeamManager()

    class Meta:
        ordering = ['-id']
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")
        unique_together = ['name', 'organization']

    def __str__(self):
        return self.name

    def is_team_member(self, member) -> bool:
        """Check if a member is part of the team."""
        return self.members.filter(
            member_id=member.id,
            is_active=True,
            member__is_active=True,
        ).exists()
