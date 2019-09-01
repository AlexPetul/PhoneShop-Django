from django.test import TestCase, Client
from django.urls import reverse
from phones_app.models import Product, Category
from django.contrib.auth.models import User
import datetime


class TestViews(TestCase):

    def setUp(self):
        test_category = Category.objects.create(
            name='Phones',
            slug='phones'
        )

        test_product = Product.objects.create(
            title='iPhone Xr',
            brand=test_category,
            image='some-image.png',
            price=666.66,
            slug='iphone-xr',
            description='dhawdawdw',
            full_description='dhuhagwiudgawk',
            time_added=datetime.datetime.now()
        )

        self.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')

        self.client = Client()

    def test_base_view(self):
        response = self.client.get(reverse('base_view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_sign_up_view(self):
        response = self.client.get(reverse('sign_up_view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

    def test_sign_in_view(self):
        response = self.client.get(reverse('sign_in_view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_detailed_product_view(self):
        response = self.client.get(
            reverse('detailed_product_view', args=['iphone-xr']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'detailed_product.html')

    def test_detailed_category_view(self):
        response = self.client.get(
            reverse('detailed_category_view', args=['phones']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'detailed_category.html')

    def test_account_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(
            reverse('account_view', args=['alexpetul']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')
