from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save


class Category(models.Model):
    name = models.CharField(max_length=15)
    slug = models.SlugField(max_length=15)

    def get_absolute_url(self):
        return reverse('detailed_category_view', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=30)
    brand = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(default='phone')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=30, blank=True, default='')
    description = models.TextField(max_length=400)
    full_description = models.TextField(max_length=2000, default='')
    time_added = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('detailed_product_view', kwargs={'product_slug': self.slug})

    def __str__(self):
        return self.title


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    products = models.ManyToManyField(CartItem, blank=True)
    total_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return '%s%d' % ('Cart', self.id)

    def add_to_cart(self, product):
        cart = self
        new_item, _ = CartItem.objects.get_or_create(
            product=product, total_price=product.price)
        if new_item not in cart.products.all():
            cart.products.add(new_item)
            cart.total_price += new_item.product.price
            cart.save()

    def remove_from_cart(self, product):
        cart = self
        for cart_item in cart.products.all():
            if cart_item.product == product:
                cart.products.remove(cart_item)
                cart_item.delete()
                cart.total_price -= cart_item.product.price
                cart.save()


def pre_save_product_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(instance.title)
        instance.slug = slug


pre_save.connect(pre_save_product_slug, sender=Product)
