from django.core.cache import cache, caches
from django.db.models.signals import post_save
from django.dispatch import receiver

from images.models import Image


@receiver(post_save, sender=Image, dispatch_uid="image_add_handler")
def image_add_handler(sender, **kwargs):
    cache.delete_many(keys=cache.keys('*.images.*'))
