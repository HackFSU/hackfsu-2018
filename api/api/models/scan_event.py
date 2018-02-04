from django.db import models
from django.contrib import admin
from django.utils import timezone
from hackfsu_com.admin import hackfsu_admin

class ScanEvent(models.Model):
    name = models.CharField(max_length=50)
    is_check_in = models.BooleanField(default=False)
    planned_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

@admin.register(ScanEvent, site=hackfsu_admin)
class ScanEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_check_in')
    # list_editable = ('name',)
    list_display_links = ('id', 'name',)
