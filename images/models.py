from django.db import models

from file_uploader import settings
from images.validators import validate_expiration_time_sec, validate_image_format


def upload_to(instance, filename):
    return f"images/user_{instance.user.id}/{filename}"


class Image(models.Model):
    image = models.ImageField(upload_to=upload_to, null=False, blank=False, default=None,
                              validators=[validate_image_format])
    user = models.ForeignKey(
        'accounts.UserAccount', on_delete=models.CASCADE, default=None
    )

    def __str__(self):
        return self.image.name

    def construct_thumbnail_url(self, size):
        return f"{settings.MEDIA_URL}{str(self.image)}/?size={size}"

    @property
    def urls(self):
        thumbnail_sizes = self.user.account_tier.thumbnail_sizes.all()
        urls = {}
        if self.user.account_tier.is_original_file_link:
            urls["original_file_link"] = self.image.url
        for size in thumbnail_sizes:
            urls[f"thumbnail_url_{size.height}"] = self.construct_thumbnail_url(size.height)
        return urls


class ThumbnailSize(models.Model):
    height = models.IntegerField()

    def __str__(self):
        return str(self.height)


class ExpiringLink(models.Model):
    link = models.CharField(max_length=255, default=None)
    image = models.ForeignKey(
        'images.Image', on_delete=models.CASCADE, default=None
    )
    expiration_time_sec = models.IntegerField(validators=[validate_expiration_time_sec])
    created_at = models.DateTimeField(auto_now_add=True)
