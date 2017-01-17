from django.db import models


class School(models.Model):
    TYPE_CHOICES = (
        ('H', 'High School'),
        ('C', 'College')
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='C')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, default='', blank=True)
