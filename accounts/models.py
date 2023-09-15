from django.db import models

import uuid


class UserAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accountTier = models.ForeignKey(
        'AccountTier', on_delete=models.CASCADE
    )


class AccountTier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_original_file_link = models.BooleanField(default=False)
    is_expiring_link = models.BooleanField(default=False)
    thumbnailSizes = models.ManyToManyField(
        'ThumbnailSize',
    )


class ThumbnailSize(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    height = models.IntegerField()
