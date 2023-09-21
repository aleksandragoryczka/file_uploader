import os

from django.core.files.uploadedfile import SimpleUploadedFile

from file_uploader import settings


def get_test_image() -> SimpleUploadedFile:
    image_path = os.path.join(settings.BASE_DIR, "images", "tests", "test-assets", "test_image.jpeg")
    simple_uploaded_file = SimpleUploadedFile(
        name="test_image.jpeg", content=open(image_path, "rb").read(), content_type="image/jpeg"
    )
    return simple_uploaded_file
