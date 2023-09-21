from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import AccountTier
from images.models import Image, ExpiringLink
from images.tests import get_test_image


class ImageAPiTestCase(APITestCase):
    def setUp(self):
        account_tier_baked = baker.make(AccountTier)
        self.user = get_user_model().objects.create_user(
            username='testusername',
            password='testpassword',
            account_tier=account_tier_baked
        )
        self.client.login(username='testusername', password='testpassword')
        self.generated_image = get_test_image()

    def test_create_image(self):
        url = reverse('create-image')
        data = {'image': self.generated_image}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)

    def test_list_images(self):
        Image.objects.create(user=self.user, image=self.generated_image)
        url = reverse('images')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ExpiringLinkAPiTestCase(APITestCase):
    def setUp(self) -> None:
        account_tier_baked = baker.make(AccountTier)
        self.user = get_user_model().objects.create_user(
            username='testusername',
            password='testpassword',
            account_tier=account_tier_baked
        )
        self.client.login(username='testusername', password='testpassword')
        self.image = Image.objects.create(user=self.user, image=get_test_image())

    def test_create_expiring_link(self):
        response = self._create_link_request(reverse('create-expiring-link'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExpiringLink.objects.count(), 1)

    def test_list_expiring_links(self):
        self._create_link_request(reverse('create-expiring-link'))
        url = reverse('expiring-link', kwargs={'image_id': self.image.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def _create_link_request(self, url):
        data = {'image': self.image.pk, 'expiration_time_sec': 3600}
        response = self.client.post(url, data, format='json')
        return response
