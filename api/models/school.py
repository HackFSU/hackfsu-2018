"""
    Good college list source: https://github.com/endSly/world-universities-csv
"""

from django.db import models
from django.contrib import admin


class School(models.Model):
    TYPE_CHOICES = (
        ('H', 'High School'),
        ('C', 'College')
    )
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='C')
    url = models.CharField(max_length=100, default='', blank=True)
    user_submitted = models.BooleanField()

    def __str__(self):
        return self.name


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_filter = ('type', 'user_submitted')
    list_display = ('name', 'type', 'user_submitted', 'url',)
    list_editable = ()
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

