from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers.organization import OrganizationManager, OrganizationProfileManager
from apps.generics.models.abstracts import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"), help_text=_("Organization name"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"), help_text=_("Organization slug"))
    owner = models.ForeignKey(
        to="accounts.Member",
        on_delete=models.CASCADE,
        related_name='owned_organizations',
        verbose_name=_("Owner"),
        help_text=_("Owner of the organization"),
        null=True,
        blank=True,
    )

    objects = OrganizationManager()

    class Meta:
        ordering = ['-id']
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self):
        return self.name

    @property
    def members(self):
        from apps.accounts.models.member import Member

        if not self.id:
            return Member.objects.none()
        return Member.objects.filter(
            organization_id=self.id,
            is_active=True,
        )


class OrganizationProfile(BaseModel):
    organization = models.OneToOneField(
        to="accounts.Organization",
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_("Organization"),
        help_text=_("Organization to which this profile belongs"),
    )
    logo = models.ImageField(
        upload_to="organization/logos",
        null=True,
        blank=True,
        verbose_name=_("Logo"),
        help_text=_("Organization logo"),
    )
    website = models.URLField(null=True, blank=True, verbose_name=_("Website"), help_text=_("Organization website"))
    description = models.TextField(
        null=True, blank=True, verbose_name=_("Description"), help_text=_("Organization description")
    )

    objects = OrganizationProfileManager()

    class Meta:
        verbose_name = _("Organization Profile")
        verbose_name_plural = _("Organization Profiles")

    def __str__(self):
        return f"{self.organization}"
