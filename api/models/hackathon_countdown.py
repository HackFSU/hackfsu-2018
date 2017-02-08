from django.db import models
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class HackathonCountdown(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.title


@admin.register(HackathonCountdown, site=hackfsu_admin)
class HackathonCountdownAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('id', 'title', 'start', 'end')
    list_editable = ('title', 'start', 'end')
    list_display_links = ('id',)
    search_fields = ('title',)
    ordering = ('hackathon', 'start')
