from django.contrib import admin
from phones_app.models import (
    Product,
    Category,
    Cart,
    CartItem,
    Order,
    ShopUser
)


def make_payed(modeladmin, request, queryset):
    queryset.update(status='Payed')


make_payed.short_description = 'Mark as payed'


class OrderAdmin(admin.ModelAdmin):
    actions = [make_payed]


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShopUser)
