from django.contrib import admin
from phones_app.models import (
    Product,
    Category,
    Cart,
    CartItem
)

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Cart)
