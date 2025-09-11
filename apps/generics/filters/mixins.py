from apps.generics.mixins.mixins import RequestUserMixin


class FilterSetMixin(RequestUserMixin):
    """Mixin for filtersets to add user, member, and organization properties."""
