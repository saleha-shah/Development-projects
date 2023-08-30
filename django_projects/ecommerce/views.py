from datetime import timedelta

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from django.db.models.signals import post_save


from ecommerce.models import Product, Order, OrderedItem
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

    if 'cart_items' not in request.session:
        request.session['cart_items'] = {}

    cart_items = request.session['cart_items']

    if product.retailer_sku in cart_items:
        cart_items[product.retailer_sku]['quantity'] += 1
    else:
        cart_items[product.retailer_sku] = {
            'retailer_sku': product.retailer_sku,
            'size': size,
            'quantity': 1
        }

    request.session.modified = True

    return redirect('ecommerce:cart')


@login_required(login_url='account:signin')
def cart(request):
    cart_items_data = request.session.get('cart_items', {})
    total_price = sum(
        Product.objects.get(retailer_sku=item['retailer_sku']).price * item['quantity']
        for item in cart_items_data.values()
    )
    context = {
        'cart_items_data': cart_items_data,
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
    cart_items_data = request.session.get('cart_items', {})

    if str(item_id) in cart_items_data:
        if action == "increase":
            cart_items_data[str(item_id)]['quantity'] += 1
        elif action == "decrease" and cart_items_data[str(item_id)]['quantity'] > 1:
            cart_items_data[str(item_id)]['quantity'] -= 1
        request.session.modified = True

    return JsonResponse({"success": True})


@login_required(login_url='account:signin')
def clear_cart(request):
    if 'cart_items' in request.session:
        del request.session['cart_items']
        request.session.modified = True

    return JsonResponse({"success": True})


@login_required(login_url='account:signin')
def delete_cart_item(request, item_id):
    cart_items_data = request.session.get('cart_items', {})

    if str(item_id) in cart_items_data:
        del cart_items_data[str(item_id)]
        request.session.modified = True

    return JsonResponse({"success": True})


@login_required(login_url='account:signin')
def checkout(request):
    cart_items_data = request.session.get('cart_items', {})
    selected_item_ids = request.GET.get('selected_items')
    selected_item_ids_list = [int(item_id) for item_id in selected_item_ids.split(',')]
    selected_cart_items = [cart_items_data[str(item_id)] for item_id in selected_item_ids_list]
    total_price = sum(
        Product.objects.get(retailer_sku=item['retailer_sku']).price * item['quantity']
        for item in selected_cart_items
    )

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        order_date = timezone.now()
        expected_delivery_date = order_date + timedelta(days=5)

        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            shipping_address = form.cleaned_data['shipping_address']
            contact_info = form.cleaned_data['contact_info']

            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    order_date=order_date,
                    expected_delivery_date=expected_delivery_date,
                    payment_method=payment_method,
                    shipping_address=shipping_address,
                    contact_info=contact_info,
                    total_price=total_price
                )

                ordered_items = [
                    OrderedItem(
                        order=order,
                        product=Product.objects.get(retailer_sku=cart_item['retailer_sku']),
                        quantity=cart_item['quantity']
                    )
                    for cart_item in selected_cart_items
                ]

                OrderedItem.objects.bulk_create(ordered_items)
                post_save.send(sender=OrderedItem, instance=ordered_items[-1], created=True)

                cart_items_data = [
                    {
                        'product_name': Product.objects.get(retailer_sku=item['retailer_sku']).name,
                        'size': item['size'],
                        'quantity': item['quantity'],
                    }
                    for item in selected_cart_items
                ]

                context = {
                    'order': order,
                    'total_price': total_price,
                    'cart_items_data': cart_items_data,
                    'total_price': total_price
                }

                return render(request, 'ecommerce/order_confirmation.html', context)

    form = CheckoutForm()
    context = {
        'form': form,
        'cart_items': selected_cart_items,
        'total_price': total_price,
    }

    return render(request, 'ecommerce/checkout.html', context)
