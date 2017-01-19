"""
    Good college list source: https://github.com/endSly/world-universities-csv
"""

from django.db import models


class School(models.Model):
    TYPE_CHOICES = (
        ('H', 'High School'),
        ('C', 'College')
    )
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='C')
    url = models.CharField(max_length=100, default='', blank=True)
    user_submitted = models.BooleanField()
