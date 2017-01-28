from django.db import models
from django.contrib import admin
from api.models import Hackathon


class ScheduleItem(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default='', blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('hackathon', 'name',  'start', 'end', 'description')
    list_editable = ('hackathon', 'start', 'end')
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('hackathon', 'start')
