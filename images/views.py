from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from file_uploader import settings
from images.mixins import ExpiringLinkMixin
from images.models import Image
from images.serializers import ImageListSerializer, ImageCreateSerializer, ExpiringLinkCreateSerializer, \
    ExpiringLinkListSerializer


class CachingBaseListApiView(ListAPIView):
    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListImageView(CachingBaseListApiView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageListSerializer

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user).all()


class CreateImageView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageCreateSerializer
    queryset = Image.objects.all()


class CreateExpiringLinkView(ExpiringLinkMixin, CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExpiringLinkCreateSerializer

    def get_queryset(self):
        return Image.objects.filter(pk=self.request.data('image_id')).all()

    def create(self, request, *args, **kwargs):
        created = super().create(request, *args, **kwargs)
        created.data['id'] = self.link.id
        img = Image.objects.get(pk=created.data['image'])
        # dbx = Dropbox(settings.DROPBOX_OAUTH2_REFRESH_TOKEN)
        # r = dbx.sharing_create_shared_link_with_settings('/images/user_2/Untitled_2.png')
        # print(r.url)
        # created.data['link'] = CustomDropboxStorage().generate_expiring_link(img, self.request.data.get('expiration_time_sec'))
        # print(created.data['link'])

        created.data['created_at'] = self.link.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return created

    def perform_create(self, serializer):
        self.link = ExpiringLinkMixin.create_expiring_link(self, self.request.data.get('image'),
                                                           int(self.request.data.get('expiration_time_sec')))


class ListExpiringLinkView(CachingBaseListApiView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExpiringLinkListSerializer

    def validate(self, image_id):
        if Image.objects.filter(pk=image_id).exists():
            if Image.objects.get(pk=image_id).user == self.request.user:
                return True
            raise serializers.ValidationError(
                {"error": "You aren't the owner of this image"}
            )
        raise serializers.ValidationError(
            {"error": f"Image with id {image_id} doesn't exist"}
        )

    def get_queryset(self):
        image_id = self.kwargs['image_id']
        if self.validate(image_id):
            return ExpiringLinkMixin.get_non_expired_links(self, image_id)
