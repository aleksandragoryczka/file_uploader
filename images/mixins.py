from django.core.signing import TimestampSigner, SignatureExpired
from rest_framework.exceptions import PermissionDenied

from file_uploader import settings
from images.models import ExpiringLink, Image
from images.utils.config import DEFAULT_EXPIRATION_TIME_SEC


class ExpiringLinkMixin:
    signer = TimestampSigner()

    def create_expiring_link(self, image_id, expiration_time_sec=DEFAULT_EXPIRATION_TIME_SEC):
        image = Image.objects.get(pk=image_id)
        if not image.user.account_tier.is_expiring_link:
            raise PermissionDenied({"error": "You don't have permission to create expiring link"})
        signed_link = self.signer.sign(f"{settings.MEDIA_URL}{image}")
        expiring_link = ExpiringLink(link=signed_link, expiration_time_sec=expiration_time_sec, image=image)
        expiring_link.save()
        return expiring_link

    def is_non_expired(expiring_link):
        try:
            ExpiringLinkMixin.signer.unsign(expiring_link.link, max_age=expiring_link.expiration_time_sec)
            return True
        except SignatureExpired:
            return False


    def get_non_expired_links(self, image_id):
        non_expired_links = ExpiringLink.objects.filter(image=image_id).all()
        return [link for link in non_expired_links if ExpiringLinkMixin.is_non_expired(link)]



