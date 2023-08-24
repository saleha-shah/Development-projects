from datetime import timedelta

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone


from ecommerce.models import Product, CartItem, Order, OrderedItem
from ecommerce.forms import CheckoutForm


def listing_page(request):
    products = Product.objects.all()

    paginator = Paginator(products, 50)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)

    products = []
    for product in pages:
        image_urls = product.image_urls.all()
        skus = product.skus.all()
        products.append({
            'product': product,
            'image_urls': image_urls,
            'skus': skus
        })

    return render(request, 'ecommerce/listings.html', {'listings': products, 'pages': pages})


def product_detail(request, product_id):
    product = Product.objects.get(retailer_sku=product_id)

    image_urls = product.image_urls.all()
    descriptions = product.description.all()
    cares = product.care.all()
    categories = product.category.all()
    skus = product.skus.all()
    data = {
        'product': product,
        'image_urls': image_urls,
        'descriptions': descriptions,
        'cares': cares,
        'categories': categories,
        'skus': skus
    }

    return render(request, 'ecommerce/product_detail.html', data)


@login_required(login_url='account:signin')
def add_to_cart(request, product_id, size):
    product = Product.objects.get(retailer_sku=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        size=size)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('ecommerce:cart')


@login_required(login_url='account:signin')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'ecommerce/cart.html', context)


def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(name__icontains=query) | Q(brand__icontains=query))
    listings = []
    for product in products:
        image_urls = product.image_urls.all()
        skus = product.skus.all()
        listings.append({
            'product': product,
            'image_urls': image_urls,
            'skus': skus
        })

    return render(request, 'ecommerce/search.html', {'listings': listings, 'query': query})


@login_required(login_url='account:signin')
def update_quantity(request, item_id, action):
    cart_item = CartItem.objects.get(id=item_id)
    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()

    return JsonResponse({"success": True})


@login_required(login_url='account:signin')
def clear_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items.delete()

    return JsonResponse({"success": True})


@login_required(login_url='account:signin')
def delete_cart_item(request, item_id):
    cart_item = CartItem.objects.filter(user=request.user, id=item_id)
    cart_item.delete()

    return JsonResponse({"success": True})


@login_required(login_url='account:signin')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        order_date = timezone.now()
        expected_delivery_date = order_date + timedelta(days=5)
        user_email = request.user.email
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            shipping_address = form.cleaned_data['shipping_address']
            contact_info = form.cleaned_data['contact_info']
            
            order = Order.objects.create(
                user=request.user,
                order_date=order_date,
                expected_delivery_date=expected_delivery_date,
                payment_method=payment_method,
                shipping_address=shipping_address,
                contact_info=contact_info,
                total_price=total_price
            )
            
            for cart_item in cart_items:
                OrderedItem.objects.create(
                    order=order,
                    cart_item=cart_item,
                    quantity=cart_item.quantity
                )

            context = {
                'order': order,
                'cart_items': cart_items,
                'total_price': total_price,
            }

            return render(request, 'ecommerce/order_confirmation.html', context)
    else:
        form = CheckoutForm()
        context = {
            'form': form,
            'cart_items': cart_items,
            'total_price': total_price,
        }

    return render(request, 'ecommerce/checkout.html', context)
