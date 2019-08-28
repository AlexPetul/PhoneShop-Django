from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from phones_app.views import (
    base_view,
    detailed_product_view,
    detailed_category_view,
    sign_up_view,
    cart_view,
    add_to_cart_view,
    remove_from_cart_view,
    increase_product_count_view,
)

urlpatterns = [
    re_path(r'^$', base_view, name='base_view'),
    re_path(r'^signup/$', sign_up_view, name='sign_up_view'),
    re_path(r'^phone/(?P<product_slug>[-\w]+)/$', detailed_product_view, name='detailed_product_view'),
    re_path(r'^category/(?P<category_slug>[-\w]+)/$', detailed_category_view, name='detailed_category_view'),
    re_path(r'^add_to_cart/$', add_to_cart_view, name='add_to_cart_view'),
    re_path(r'^add_qty_to_product/$', increase_product_count_view, name='increase_product_count_view'),
    re_path(r'^remove_from_cart/$', remove_from_cart_view, name='remove_from_cart_view'),
    re_path(r'^cart/$', cart_view, name='cart_view'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
