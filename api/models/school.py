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
        summary = "{} - {}".format(
            self.type,
            self.name
        )

        if self.user_submitted:
            summary += ' - USER SUBMITTED'

        return summary


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_filter = ('type', 'user_submitted')
