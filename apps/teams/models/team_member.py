from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.generics.models.abstracts import BaseModel
from apps.teams.choices import TeamMemberRoleChoices
from apps.teams.managers.team_member import TeamMemberManager


class TeamMember(BaseModel):
    team = models.ForeignKey(
        to="teams.Team",
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name=_("Team"),
        help_text=_("Team to which this member belongs"),
    )
    member = models.ForeignKey(
        to="accounts.Member",
        on_delete=models.CASCADE,
        related_name='teams',
        verbose_name=_("Member"),
        help_text=_("Member of the team"),
    )
    role = models.CharField(
        max_length=20,
        verbose_name=_("Role"),
        help_text=_("Role of the member in the team"),
        choices=TeamMemberRoleChoices.choices,
        default=TeamMemberRoleChoices.MEMBER,
    )

    objects = TeamMemberManager()

    class Meta:
        ordering = ['-id']
        verbose_name = _("Team Member")
        verbose_name_plural = _("Team Members")
        unique_together = ['team', 'member']

    def __str__(self):
        return f"{self.member} - {self.team}"

    @property
    def is_owner(self) -> bool:
        return self.role == TeamMemberRoleChoices.OWNER

    @property
    def is_admin(self) -> bool:
        return self.role == TeamMemberRoleChoices.ADMIN

    @property
    def is_manager(self) -> bool:
        return self.role == TeamMemberRoleChoices.MANAGER

    @property
    def is_member(self) -> bool:
        return self.role == TeamMemberRoleChoices.MEMBER

    @property
    def has_owner_permission(self) -> bool:
        return self.is_owner or self.member.has_admin_permission

    @property
    def has_admin_permission(self) -> bool:
        return self.is_admin or self.has_owner_permission

    @property
    def has_manager_permission(self) -> bool:
        return self.is_manager or self.has_admin_permission

    @property
    def has_member_permission(self) -> bool:
        return self.is_member or self.has_manager_permission

    @classmethod
    def label_expression(cls) -> models.expressions.Combinable:
        """
        Get the label expression for the team member.
        """
        from apps.accounts.models.member import Member

        return Member.label_expression(outer_ref="member")
