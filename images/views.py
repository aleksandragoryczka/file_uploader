from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from images.mixins import ExpiringLinkMixin
from images.models import Image
from images.serializers import ImageListSerializer, ImageCreateSerializer, ExpiringLinkCreateSerializer, \
    ExpiringLinkListSerializer


class ListImageView(ListAPIView):
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
        created.data['link'] = self.link.link
        created.data['created_at'] = self.link.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return created

    def perform_create(self, serializer):
        self.link = ExpiringLinkMixin.create_expiring_link(self, self.request.data.get('image'),
                                                           int(self.request.data.get('expiration_time_sec')))


class ListExpiringLinkView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExpiringLinkListSerializer

    def get_queryset(self):
        image_id = self.request.data.get('image')
        print(self.request.data)
        print(self.request.query_params)
        return ExpiringLinkMixin.get_non_expired_links(self, image_id)

