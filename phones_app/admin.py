from django.contrib import admin
from phones_app.models import (
    Product,
    Category,
    Cart,
    CartItem,
    Order
)

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)