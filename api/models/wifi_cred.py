from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from api.models import Hackathon


class WifiCred(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    assigned_user = models.OneToOneField(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return '[WifiCred {}]'.format(self.username)


@admin.register(WifiCred)
class WifiCredAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('username', 'assigned_user',)
    list_editable = ()
    list_display_links = ('username',)
    search_fields = ('assigned_user',)
    ordering = ('assigned_user',)

