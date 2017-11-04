"""
    Good college list source: https://github.com/endSly/world-universities-csv
"""

from django.db import models
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin
from api.models import Hackathon, AttendeeStatus


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


@admin.register(School, site=hackfsu_admin)
class SchoolAdmin(admin.ModelAdmin):
    list_filter = ('type', 'user_submitted')
    list_display = (
        'name', 'type', 'user_submitted', 'url',
        'current_hackers_registered', 'current_hackers_rsvp', 'current_hackers_checked_in'
    )
    list_editable = ()
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

    @staticmethod
    def current_hackers_registered(obj):
        h = Hackathon.objects.current()
        return AttendeeStatus.objects.filter(hackathon=h, hackerinfo__isnull=False, hackerinfo__school=obj).count()

    @staticmethod
    def current_hackers_rsvp(obj):
        h = Hackathon.objects.current()
        return AttendeeStatus.objects.filter(
            hackathon=h, rsvp_result=True, hackerinfo__isnull=False, hackerinfo__school=obj,
        ).count()

    @staticmethod
    def current_hackers_checked_in(obj):
        h = Hackathon.objects.current()
        return AttendeeStatus.objects.filter(
            hackathon=h, checked_in_at__isnull=False, hackerinfo__isnull=False, hackerinfo__school=obj,
        ).count()
