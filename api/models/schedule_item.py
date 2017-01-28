from django.db import models
from django.contrib import admin
from api.models import Hackathon


class ScheduleItem(models.Model):

    EVENT_TYPE = (
        (0, 'Key'),
        (1, 'Tech Talk'),
        (2, 'Food'),
        (3, 'Social'),
        (4, 'Miscellaneous')
    )

    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default='', blank=True)
    type = models.SmallIntegerField(default=0, choices=EVENT_TYPE)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('hackathon', 'type', 'name', 'start', 'end', 'description')
    list_editable = ('start', 'end')
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('hackathon', 'start')
