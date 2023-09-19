from django.db import models

from images.dropbox_api import DropboxAPI
from images.validators import validate_expiration_time_sec, validate_image_format


def upload_to(instance, filename):
    print("KOT")
    return f"images/user_{instance.user.id}/{filename}"


class ThumbnailURL(models.Model):
    image = models.ForeignKey('images.Image', on_delete=models.CASCADE)
    size = models.CharField(max_length=20)
    url = models.URLField()


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
        thumbnail_urls = ThumbnailURL.objects.filter(image=self).all()
        if thumbnail_urls:
            for thumbnail_url in thumbnail_urls:
                urls[f"thumbnail_url_{thumbnail_url.size}"] = thumbnail_url.url
        return urls

    def create_urls(self):
        thumbnail_sizes = self.user.account_tier.thumbnail_sizes.all()

        for size in thumbnail_sizes:
            dbx = DropboxAPI()
            generated_thumbnail_url = dbx.generate_thumbnail_url('/' + self.image.name, size.dimension)
            ThumbnailURL.objects.create(image=self, size=size.dimension, url=generated_thumbnail_url)



class ThumbnailSize(models.Model):
    dimension = models.CharField(max_length=50)

    def __str__(self):
        return str(self.dimension)


class ExpiringLink(models.Model):
    link = models.CharField(max_length=255, default=None)
    image = models.ForeignKey(
        'images.Image', on_delete=models.CASCADE, default=None
    )
    expiration_time_sec = models.IntegerField(validators=[validate_expiration_time_sec])
    created_at = models.DateTimeField(auto_now_add=True)
