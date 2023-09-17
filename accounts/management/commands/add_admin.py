from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Add init admin user"

    def handle(self, *args, **options):
        username = "admin"
        password = "admin"
        email = "admin@email.com"
        if not get_user_model().objects.filter(username=username).exists():
            get_user_model().objects.create_superuser(
                username=username, email=email, password=password
            )
