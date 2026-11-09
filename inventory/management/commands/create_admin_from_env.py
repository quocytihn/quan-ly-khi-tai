import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Create the initial admin from ADMIN_USERNAME, ADMIN_EMAIL and ADMIN_PASSWORD environment variables."

    def handle(self, *args, **options):
        username = os.getenv("ADMIN_USERNAME", "admin").strip()
        email = os.getenv("ADMIN_EMAIL", "admin@example.com").strip()
        password = os.getenv("ADMIN_PASSWORD", "")
        if not password:
            self.stdout.write(self.style.WARNING("ADMIN_PASSWORD is not set; skipping admin creation."))
            return
        if len(password) < 12:
            raise CommandError("ADMIN_PASSWORD must contain at least 12 characters.")
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Admin '{username}' already exists; password was not changed."))
            return
        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
