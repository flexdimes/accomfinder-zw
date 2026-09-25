import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Creates (or updates the password for) an admin account from environment
    variables, so you can log into /admin/ without needing Shell access
    (Shell is a paid-plan-only feature on Render).

    Set these as environment variables on your host, then remove them again
    after the first successful deploy — they're only needed once:
      DJANGO_SUPERUSER_USERNAME
      DJANGO_SUPERUSER_EMAIL      (optional)
      DJANGO_SUPERUSER_PASSWORD

    If these variables aren't set, this command does nothing — safe to run
    on every deploy without side effects.
    """
    help = "Create or update an admin account from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write("No DJANGO_SUPERUSER_USERNAME/PASSWORD set — skipping admin setup.")
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created admin account '{username}'."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated password for existing admin account '{username}'."))
