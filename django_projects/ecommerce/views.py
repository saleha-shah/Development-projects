from django.shortcuts import render
from django.core.paginator import Paginator

from ecommerce.models import Product


def listing_page(request):
    products = Product.objects.all()

    paginator = Paginator(products, 50)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)

    products = []
    for product in pages:
        image_urls = product.image_urls.all()
        products.append({
            'product': product,
            'image_urls': image_urls
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
