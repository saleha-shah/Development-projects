from django.db import models
from django.contrib.auth.models import User


class ProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, default='O')
    dob = models.DateField(default=None)
