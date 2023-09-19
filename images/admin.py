from django.contrib import admin

from images.models import ExpiringLink, Image

admin.site.register([Image, ExpiringLink])
