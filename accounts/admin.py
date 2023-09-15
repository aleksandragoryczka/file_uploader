from django.contrib import admin

from accounts.models import AccountTier, ThumbnailSize, UserAccount

admin.site.register([AccountTier, UserAccount, ThumbnailSize])
