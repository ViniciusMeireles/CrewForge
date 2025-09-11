from urllib.request import Request

from apps.accounts.models.member import Member
from apps.accounts.models.organization import Organization


def get_organization_id(request: Request) -> int | None:
    """Get the organization ID from the request."""
    if not request or not request.user.is_authenticated:
        return None
    return request.session.get("organization_id")


def get_organization(request: Request) -> Organization | None:
    """Get the organization from the request."""
    if not (organization_id := get_organization_id(request)):
        return None
    return request.user.organizations.get_or_none(id=organization_id)


def get_member(request: Request) -> Member | None:
    """Get the member from the request."""
    user = request.user
    if not user.is_authenticated:
        return None
    if not (organization_id := request.session.get("organization_id")):
        return None
    return user.members.get_or_none(organization_id=organization_id)
