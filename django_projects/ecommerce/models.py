import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    brand = models.CharField(max_length=250)
    currency = models.CharField(max_length=3)
    lang = models.CharField(max_length=2)
    market = models.CharField(max_length=2)
    name = models.CharField(max_length=500)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    gender = models.CharField(max_length=6)
    retailer_sku = models.CharField(max_length=20, unique=True, primary_key=True)
    trail = models.CharField(max_length=500)
    url = models.TextField()


class ImageURL(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image_urls')
    color = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.url


class SKU(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='skus')
    sku = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    size = models.CharField(max_length=10)
    currency = models.CharField(max_length=3)
    out_of_stock = models.BooleanField()

    def __str__(self):
        sku_dict = {
            'sku': self.sku,
            'color': self.color,
            'price': self.price,
            'size': self.size,
            'currency': self.currency,
            'out_of_stock': self.out_of_stock,
        }
        return str(sku_dict)


class Description(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='description')
    content = models.CharField(max_length=250)

    def __str__(self):
        return self.content


class Care(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='care')
    content = models.CharField(max_length=250)

    def __str__(self):
        return self.content


class Category(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='category')
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    size = models.CharField(max_length=10, default='One Size')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    shipping_address = models.TextField()
    contact_info = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    expected_delivery_date = models.DateTimeField()

    def __str__(self):
        return f"Order ID: {self.order_id}"


class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cart_item.product.name} - {self.quantity}"
