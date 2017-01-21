from django.db import models
from django.contrib.auth.models import User
from api.models import Hackathon


class UserInfo(models.Model):
    SHIRT_SIZE_CHOICES = (
        ('m-s',     'Men\'s Small'),
        ('m-m',     'Men\'s Medium'),
        ('m-l',     'Men\'s Large'),
        ('m-xl',    'Men\'s XL'),
        ('m-2xl',   'Men\'s XXL'),
        ('m-3xl',   'Men\'s XXXL'),
        ('w-s',     'Women\'s Small'),
        ('w-m',     'Women\'s Medium'),
        ('w-l',     'Women\'s Large'),
        ('w-xl',    'Women\'s XL')
    )

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    shirt_size = models.CharField(max_length=3, choices=SHIRT_SIZE_CHOICES)
    diet = models.CharField(max_length=500, default='', blank=True)
    github = models.CharField(max_length=100, default='', blank=True)
    linkedin = models.CharField(max_length=100, default='', blank=True)
    last_hackathon = models.ForeignKey(to=Hackathon, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    comments = models.CharField(max_length=1000, default='', blank=True)
