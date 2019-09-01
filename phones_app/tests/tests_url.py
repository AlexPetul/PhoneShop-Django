from django.test import Client, SimpleTestCase
from django.urls import reverse, resolve
from phones_app.views import (
    base_view,
    detailed_product_view,
    detailed_category_view,
    sign_up_view,
    cart_view,
    add_to_cart_view,
    remove_from_cart_view,
    increase_product_count_view,
    decrease_product_count_view,
    checkout_view,
    make_order_view,
    logout_view,
    sign_in_view,
    account_view
)


class TestUrls(SimpleTestCase):

    def test_base_url(self):
        url = reverse('base_view')
        self.assertEquals(resolve(url).func, base_view)

    def test_product_url(self):
        url = reverse('detailed_product_view', args=['some-product-slug'])
        self.assertEquals(resolve(url).func, detailed_product_view)

    def test_category_url(self):
        url = reverse('detailed_category_view', args=['some-category-slug'])
        self.assertEquals(resolve(url).func, detailed_category_view)

    def test_account_url(self):
        url = reverse('account_view', args=['some-username'])
        self.assertEquals(resolve(url).func, account_view)

    def test_add_qty_url(self):
        url = reverse('increase_product_count_view')
        self.assertEquals(resolve(url).func, increase_product_count_view)

    def test_remove_qty_url(self):
        url = reverse('decrease_product_count_view')
        self.assertEquals(resolve(url).func, decrease_product_count_view)

    def test_remove_from_cart_url(self):
        url = reverse('remove_from_cart_view')
        self.assertEquals(resolve(url).func, remove_from_cart_view)

    def test_cart_url(self):
        url = reverse('cart_view')
        self.assertEquals(resolve(url).func, cart_view)

    def test_add_to_cart_url(self):
        url = reverse('add_to_cart_view')
        self.assertEquals(resolve(url).func, add_to_cart_view)

    def test_checkout_url(self):
        url = reverse('checkout_view')
        self.assertEquals(resolve(url).func, checkout_view)

    def test_order_url(self):
        url = reverse('make_order_view')
        self.assertEquals(resolve(url).func, make_order_view)

    def test_signin_url(self):
        url = reverse('sign_in_view')
        self.assertEquals(resolve(url).func, sign_in_view)

    def test_signup_url(self):
        url = reverse('sign_up_view')
        self.assertEquals(resolve(url).func, sign_up_view)

    def test_logout_url(self):
        url = reverse('logout_view')
        self.assertEquals(resolve(url).func, logout_view)
