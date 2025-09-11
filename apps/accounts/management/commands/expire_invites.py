from django.core.management import BaseCommand

from apps.accounts.models.invitation import Invitation


class Command(BaseCommand):
    help = "Expire all pending invites that are past their expiration date."

    def handle(self, *args, **options):
        from django.utils import timezone

        expired_invites = Invitation.objects.filter(
            is_active=True,
            is_expired=False,
            expired_at__lt=timezone.now(),
        )

        count_expired = expired_invites.update(is_expired=True)
        self.stdout.write(self.style.SUCCESS(f"Expired {count_expired} invites."))
