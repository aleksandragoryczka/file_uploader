from rest_framework import serializers

from images.utils.config import MIN_EXPIRATION_TIME_SEC, MAX_EXPIRATION_TIME_SEC, VALID_IMAGE_FORMATS


def validate_expiration_time_sec(value):
    if MIN_EXPIRATION_TIME_SEC <= value <= MAX_EXPIRATION_TIME_SEC:
        return value
    raise serializers.ValidationError(
        {"error": f"expiration_time_sec must be greater or equal than {MIN_EXPIRATION_TIME_SEC} "
                  f"and less or equal than {MAX_EXPIRATION_TIME_SEC}"})


def validate_image_format(image):
    if any([image.name.endswith(ext) for ext in VALID_IMAGE_FORMATS]):
        return True
    raise serializers.ValidationError(
        {"error": f"Image format must be one of {VALID_IMAGE_FORMATS}"}
    )
