from django.db import models
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class Subscriber(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[{} Subscriber, {}]'.format(self.hackathon, self.email)


@admin.register(Subscriber, site=hackfsu_admin)
class SubscriberAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('email', 'hackathon', 'created')
    list_editable = ()
    list_display_links = ('email',)
    search_fields = ('email',)
    ordering = ('-created',)

