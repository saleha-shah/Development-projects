from django.db import models
from django.contrib.auth.models import User


class ProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, default='O')
    dob = models.DateField(default=None)


class Listing(models.Model):
    brand = models.CharField(max_length=500)
    care = models.CharField(max_length=500)
    category = models.TextField()
    currency = models.CharField(max_length=3)
    description = models.TextField()
    image_urls = models.TextField()
    lang = models.CharField(max_length=2)
    market = models.CharField(max_length=2)
    name = models.CharField(max_length=500)
    price = models.FloatField()
    retailer_sku = models.CharField(max_length=20, unique=True)
    skus = models.CharField(max_length=100)
    trail = models.CharField(max_length=500)
    url = models.TextField()
