from django.db import models
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class PreviewEmail(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    interest = models.CharField(max_length=100)
    submit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[PreviewEmail {} - {}]'.format(self.email, self.interest)


@admin.register(PreviewEmail, site=hackfsu_admin)
class PreviewEmailAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('id', 'email', 'interest', 'submit_time')
    list_editable = ('email', 'interest')
    list_display_links = ('id',)
    search_fields = ('email', 'interest')
    ordering = ('-submit_time',)
