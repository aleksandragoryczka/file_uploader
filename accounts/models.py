from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid
from images.models import ThumbnailSize


class UserAccount(AbstractUser):
    account_tier = models.ForeignKey(
        'AccountTier', on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        try:
            return f"{self.id} {self.username} - {self.account_tier.name}"
        except AttributeError:
            return self.username


class AccountTier(models.Model):
    name = models.CharField(max_length=255)
    is_original_file_link = models.BooleanField(default=False)
    is_expiring_link = models.BooleanField(default=False)
    thumbnail_sizes = models.ManyToManyField(
        'images.ThumbnailSize',
        related_name='account_tier',
    )

    def __str__(self):
        return self.name
