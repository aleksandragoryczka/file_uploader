from django.core.management.base import BaseCommand

from images.mixins import ExpiringLinkMixin
from images.models import ExpiringLink


class Command(BaseCommand):
    help = "Remove expired links from database"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        expired_links_ids = [link.id for link in ExpiringLink.objects.all() if
                             not ExpiringLinkMixin.is_non_expired(link)]
        ExpiringLink.objects.filter(pk__in=expired_links_ids).delete()
