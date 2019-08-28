from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from phones_app.models import (
    Product,
    Category,
    Cart,
    CartItem
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
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'cart': cart
    }
    return render(request, 'index.html', context)


def sign_up_view(request):
    login_form = UserCreationForm(request.POST or None)
    if login_form.is_valid():
        user = login_form.save()
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
