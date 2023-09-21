from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker

from accounts.models import AccountTier
from images.models import Image
from images.tests.test_utils import get_test_image


class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        account_tier_baked = baker.make(AccountTier)
        cls.user = get_user_model().objects.create_user(username='testusername',
                                                        password='testpassword',
                                                        account_tier=account_tier_baked)
        cls.image = Image.objects.create(image=get_test_image(), user=cls.user)

    def test_image_str_method(self):
        expected_str = f"{self.image.image.name}"
        self.assertEqual(expected_str, str(self.image))
