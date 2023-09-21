from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from accounts.models import AccountTier
from images.models import ThumbnailSize


class UserAccountTiersTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'fixtures/account_tier_fixture.json', 'fixtures/thumbnail_size_fixture.json')
        cls.user_basic = get_user_model().objects.create_user(username='basic', password='testpassword',
                                                              account_tier=AccountTier.objects.get(name='Basic'))
        cls.user_premium = get_user_model().objects.create_user(username='premium', password='testpassword',
                                                                account_tier=AccountTier.objects.get(name='Premium'))
        cls.user_enterprise = get_user_model().objects.create_user(
            username='enterprise', password='testpassword', account_tier=AccountTier.objects.get(name='Enterprise'))

    def test_create_user_account_tiers_values(self):
        self.assertEqual(self.user_basic.account_tier.name, 'Basic')
        self.assertEqual(self.user_premium.account_tier.name, 'Premium')
        self.assertEqual(self.user_enterprise.account_tier.name, 'Enterprise')
        self.assertEqual(self.user_basic.account_tier.is_original_file_link, False)
        self.assertEqual(self.user_premium.account_tier.is_original_file_link, True)
        self.assertEqual(self.user_enterprise.account_tier.is_original_file_link, True)
        self.assertEqual(self.user_basic.account_tier.is_expiring_link, False)
        self.assertEqual(self.user_premium.account_tier.is_expiring_link, False)
        self.assertEqual(self.user_enterprise.account_tier.is_expiring_link, True)

    def test_account_tier_thumbnail_sizes(self):
        basic_thumbnail_sizes = [size.height for size in self.user_basic.account_tier.thumbnail_sizes.all()]
        premium_thumbnail_sizes = [size.height for size in self.user_premium.account_tier.thumbnail_sizes.all()]
        enterprise_thumbnail_sizes = [size.height for size in self.user_enterprise.account_tier.thumbnail_sizes.all()]

        self.assertEqual(basic_thumbnail_sizes, ['200'])
        self.assertEqual(premium_thumbnail_sizes, ['200', '400'])
        self.assertEqual(enterprise_thumbnail_sizes, ['200', '400'])

    def test_create_new_account_tier(self):
        account_tier = AccountTier.objects.create(
            name='Premium+',
            is_original_file_link=False,
            is_expiring_link=True,
        )
        account_tier.thumbnail_sizes.set(ThumbnailSize.objects.filter(height__in=[200, 400]))
        self.assertEqual(account_tier.name, 'Premium+')
        self.assertFalse(account_tier.is_original_file_link)
        self.assertTrue(account_tier.is_expiring_link)
        self.assertEqual(account_tier.thumbnail_sizes.count(), 2)