from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate
from phones_app.forms import OrderForm
from django.contrib.auth.forms import UserCreationForm
from phones_app.models import (
    Product,
    Category,
    Cart,
    CartItem,
    Order,
    ShopUser
)


def get_users_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.products.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart


def base_view(request):
    cart = get_users_cart(request)
    products = Product.objects.order_by('-time_added')[:3]
    carousel_products = Product.objects.order_by('time_added')[:3]
    print(carousel_products)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'cart': cart,
        'carousel_products': carousel_products
    }
    return render(request, 'index.html', context)


def sign_up_view(request):
    login_form = UserCreationForm(request.POST or None)
    if login_form.is_valid():
        user = login_form.save()
        shop_user = ShopUser()
        shop_user.user = user
        shop_user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('base_view'))
    context = {
        'login_form': login_form
    }
    return render(request, 'registration.html', context)


def detailed_product_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    context = {
        'product': product
    }
    return render(request, 'detailed_product.html', context)


def detailed_category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products_of_category = category.product_set.all()
    context = {
        'category': category,
        'products': products_of_category
    }
    return render(request, 'detailed_category.html', context)


def cart_view(request):
    cart = get_users_cart(request)
    cart_products = cart.products.all()
    context = {
        'cart': cart,
        'products': cart_products
    }
    return render(request, 'cart.html', context)


def add_to_cart_view(request):
    cart = get_users_cart(request)
    product_slug = request.GET.get('product_slug')
    print(product_slug)
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product)
    return JsonResponse({'total': cart.products.count()})


def increase_product_count_view(request):
    cart = get_users_cart(request)
    cart_item_id = request.GET.get('item_id')
    cart_item = cart.products.get(id=cart_item_id)
    cart_item.count += 1
    cart_item.total_price += cart_item.product.price
    cart.total_price += cart_item.product.price
    cart_item.save()
    cart.save()
    return JsonResponse({
        'count': cart_item.count,
        'product_total_price': cart_item.total_price,
        'total_cart_price': cart.total_price
    })


def decrease_product_count_view(request):
    cart = get_users_cart(request)
    cart_item_id = request.GET.get('item_id')
    cart_item = cart.products.get(id=cart_item_id)
    if cart_item.count != 1:
        cart_item.count -= 1
        cart_item.total_price -= cart_item.product.price
        cart.total_price -= cart_item.product.price
        cart_item.save()
        cart.save()
        return JsonResponse({
            'count': cart_item.count,
            'product_total_price': cart_item.total_price,
            'total_cart_price': cart.total_price
        })


def remove_from_cart_view(request):
    cart = get_users_cart(request)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product)
    return JsonResponse({
        'total': cart.products.count(),
        'total_cart_price': cart.total_price
    })


def checkout_view(request):
    cart = get_users_cart(request)
    products = cart.products.all()
    context = {
        'cart': cart,
        'products': products
    }
    return render(request, 'checkout.html', context)


def make_order_view(request):
    cart = get_users_cart(request)
    order_form = OrderForm(request.POST or None)
    if order_form.is_valid():
        first_name = order_form.cleaned_data.get('first_name')
        last_name = order_form.cleaned_data.get('last_name')
        phone = order_form.cleaned_data.get('phone')
        address = order_form.cleaned_data.get('address')
        buying_type = order_form.cleaned_data.get('buying_type')
        comment = order_form.cleaned_data.get('comment')
        new_order = Order()
        new_order.user = request.user
        new_order.first_name = first_name
        new_order.last_name = last_name
        new_order.phone = phone
        new_order.address = address
        new_order.buying_type = buying_type
        new_order.comment = comment
        new_order.total = cart.products.count()
        del request.session['cart_id']
        del request.session['total']
        return HttpResponseRedirect(reverse('base_view'))

    context = {
        'order_form': order_form
    }
    return render(request, 'order.html', context)
