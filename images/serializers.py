from rest_framework import serializers

from images.models import Image, ExpiringLink


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
        image_instance = Image(**validated_data)
        image_instance.save()
        image_instance.create_urls()
        return image_instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('image')
        representation['urls'] = instance.urls
        return representation


class ExpiringLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['expiration_time_sec', 'image']


class ExpiringLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['id', 'expiration_time_sec', 'link', 'created_at']

    def validate(self, **kwargs):
        if Image.objects.get(pk=self.kwargs['image_id']).user == self.request.user:
            return True
        raise serializers.ValidationError(
            {"error": "You aren't the owner of this image"}
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return representation


