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
        return image_instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('image')
        representation['urls'] = instance.urls
        return representation


class ExpiringLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['image', 'expiration_time_sec']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(user=self.context['request'].user)


class ExpiringLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['id', 'expiration_time_sec', 'link', 'expiration_time']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['expiration_time'] = instance.expiration_time.strftime("%Y-%m-%d %H:%M:%S")
        return representation

