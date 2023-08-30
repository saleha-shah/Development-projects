from django import template
from ecommerce.models import Product

register = template.Library()


@register.filter
def get_product(retailer_sku):
    return Product.objects.get(retailer_sku=retailer_sku)
