from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from file_uploader import settings
from images.dropbox_api import DropboxAPI
from images.models import Image, ExpiringLink
from images.serializers import ImageListSerializer, ImageCreateSerializer, ExpiringLinkCreateSerializer, \
    ExpiringLinkListSerializer


class ListImageView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageListSerializer

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user).all()

    @method_decorator(cache_page(settings.CACHE_TTL, key_prefix="images"))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CreateImageView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageCreateSerializer
    queryset = Image.objects.all()


class CreateExpiringLinkView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExpiringLinkCreateSerializer
    queryset = Image.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["image_id"] = response.data['image']
        response.data['image'] = Image.objects.get(pk=response.data['image']).image.name
        response.data['link'] = self.expiring_link[0]
        response.data['expiration_time'] = self.expiring_link[1].strftime("%Y-%m-%d %H:%M:%S")
        return response

    def perform_create(self, serializer):
        image_instance = Image.objects.get(pk=self.request.data['image'])
        try:
            generated_link = DropboxAPI().create_expiring_link('/' + image_instance.image.name,
                                                      self.request.data.get('expiration_time_sec'))
            ExpiringLink.objects.create(link=generated_link[0],
                                        expiration_time_sec=self.request.data.get('expiration_time_sec'),
                                        image=image_instance,
                                        expiration_time=generated_link[1])
            self.expiring_link = generated_link

        except Exception as e:
            raise serializers.ValidationError(
                {"error": f"Expiring link for that image already exists. "
                          f"Fetch it with url: http://127.0.0.1:8000/api/images/expiring-link/{image_instance.pk}"}
            )


class ListExpiringLinkView(ListAPIView):
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
            return ExpiringLink.objects.filter(image=image_id).all()
