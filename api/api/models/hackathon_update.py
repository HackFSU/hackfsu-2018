from django.db import models
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class HackathonUpdate(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    submit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[HackathonUpdate {} - {}]'.format(self.submit_time, self.title)


@admin.register(HackathonUpdate, site=hackfsu_admin)
class HackathonUpdateAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('id', 'title', 'content', 'submit_time')
    list_editable = ('title', 'content')
    list_display_links = ('id',)
    search_fields = ('title', 'content')
    ordering = ('-submit_time',)
