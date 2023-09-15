import uuid

from django.db import models


# Create your models here.
class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   # image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(
       'accounts.UserAccount', on_delete=models.CASCADE
    )


class ExpiringLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expiration_time = models.DateTimeField()
    image = models.ForeignKey(
        'images.Image', on_delete=models.CASCADE
    )
