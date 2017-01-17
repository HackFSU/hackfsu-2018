from django.db import models
from django.contrib.auth.models import User


class MentorInfo(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=100)
    comments = models.CharField(max_length=1000, default='', blank=True)
