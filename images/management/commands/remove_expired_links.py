from datetime import datetime

from django.core.management.base import BaseCommand

from images.models import ExpiringLink


class Command(BaseCommand):
    help = "Remove expired links from database"

    def handle(self, *args, **options):
        expired_links_ids = ExpiringLink.objects.filter(expiration_time__lt=datetime.now()).values_list('id', flat=True)
        ExpiringLink.objects.filter(pk__in=expired_links_ids).delete()
