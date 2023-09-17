from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from accounts.forms import AdminUserCreationForm
from accounts.models import AccountTier, ThumbnailSize, UserAccount
from django.utils.translation import gettext_lazy as _


class AdminUserDetails(UserAdmin):
    add_form = AdminUserCreationForm
    model = UserAccount
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_superuser",
                ),
            },
        ),
    ) + ((None, {"fields": ("account_tier",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("account_tier",)}),)
    list_display = ("username", "account_tier", "is_superuser",)


admin.site.register(UserAccount, AdminUserDetails)
admin.site.register([AccountTier])
admin.site.unregister([Group, Site])
admin.site.site_header = 'File Uploader Admin Panel'
