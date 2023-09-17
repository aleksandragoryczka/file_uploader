from rest_framework import serializers

from images.models import Image, ExpiringLink
from images.utils.config import VALID_IMAGE_FORMATS
from images.validators import validate_image_format, validate_expiration_time_sec


class ImageListSerializer(serializers.ModelSerializer):
    urls = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'urls']

    def urls(self, obj):
        return obj.urls


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Image.objects.create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('image')
        representation['urls'] = instance.urls
        return representation


class ExpiringLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['expiration_time_sec', 'image']

    def validate_expiration_time_sec(self, value):
        if validate_expiration_time_sec(value):
            return value


class ExpiringLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['id', 'expiration_time_sec', 'link', 'created_at']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(self.get_validators())
        representation['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return representation


