from django.db import models
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class HackathonPrize(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    award_giver = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)


@admin.register(HackathonPrize, site=hackfsu_admin)
class HackathonPrizeAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('id', 'award_giver', 'title', 'description')
    list_editable = ('award_giver', 'title', 'description')
    list_display_links = ('id',)
    search_fields = ('award_giver', 'title', 'description')
    ordering = ('award_giver',)
