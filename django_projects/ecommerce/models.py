from django.db import models


class Product(models.Model):
    brand = models.CharField(max_length=500)
    currency = models.CharField(max_length=3)
    lang = models.CharField(max_length=2)
    market = models.CharField(max_length=2)
    name = models.CharField(max_length=500)
    price = models.FloatField()
    retailer_sku = models.CharField(max_length=20, unique=True, primary_key=True)
    trail = models.CharField(max_length=500)
    url = models.TextField()


class ImageURL(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image_urls')
    color = models.CharField(max_length=50)
    url = models.URLField()


class SKU(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='skus')
    sku = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    price = models.FloatField()
    size = models.CharField(max_length=10)
    currency = models.CharField(max_length=3)
    out_of_stock = models.BooleanField()


class Description(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='description')
    content = models.CharField(max_length=250)


class Care(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='care')
    content = models.CharField(max_length=250)


class Category(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='category')
    category = models.CharField(max_length=50)
