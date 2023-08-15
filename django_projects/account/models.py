from django.db import models
from django.contrib.auth.models import User


class ProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, default='O')
    dob = models.DateField(default=None)


class Listing(models.Model):
    brand = models.CharField(max_length=500)
    care = models.CharField(max_length=500)
    category = models.CharField(max_length=500)
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=1000)
    image_urls = models.CharField(max_length=1000)
    lang = models.CharField(max_length=2)
    market = models.CharField(max_length=2)
    name = models.CharField(max_length=500)
    price = models.FloatField()
    retailer_sku = models.CharField(max_length=20)
    skus = models.CharField(max_length=100)
    trail = models.CharField(max_length=500)
    url = models.TextField()
