from django.db import models
from django.contrib.auth.models import User


class WifiCred(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    assigned_user = models.OneToOneField(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
