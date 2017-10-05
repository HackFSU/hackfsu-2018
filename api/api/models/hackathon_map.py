from django.db import models
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class HackathonMap(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    order = models.SmallIntegerField()

    def __str__(self):
        return '[HackathonMap {}]'.format(self.title)


@admin.register(HackathonMap, site=hackfsu_admin)
class HackathonMapAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('id', 'title', 'link', 'order')
    list_editable = ('title', 'link', 'order')
    list_display_links = ('id',)
    search_fields = ('title',)
    ordering = ('hackathon', 'title')
