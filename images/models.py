from django.db import models

from images.validators import validate_expiration_time_sec, validate_image_format

from sorl.thumbnail import get_thumbnail


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

    @property
    def urls(self):
        urls = {}
        if self.user.account_tier.is_original_file_link:
            urls["original_file_link"] = self.image.url
        thumbnail_sizes = self.user.account_tier.thumbnail_sizes.all()
        if self.image:
            for size in thumbnail_sizes:
                urls[f"thumbnail_url_{size}"] = get_thumbnail(self.image, f"{size}").url
        return urls


class ThumbnailSize(models.Model):
    height = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.height}x{self.height}"


class ExpiringLink(models.Model):
    link = models.CharField(max_length=500, default=None)
    image = models.ForeignKey(
        'images.Image', on_delete=models.CASCADE, default=None
    )
    expiration_time_sec = models.IntegerField(validators=[validate_expiration_time_sec])
    expiration_time = models.DateTimeField()
