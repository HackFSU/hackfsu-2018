from django.db import models
from api.models import UserInfo, ScanEvent
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin

class ScanRecord(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    scan_event = models.ForeignKey(to='api.ScanEvent', on_delete=models.CASCADE)
    user_info = models.ForeignKey(to='api.UserInfo', on_delete=models.CASCADE)


@admin.register(ScanRecord, site=hackfsu_admin)
class ScanRecordAdmin(admin.ModelAdmin):
    list_filter = ('scan_event__name',)
    list_display = ('id', 'event_name', 'user_name')
    list_display_links = ('id',)
    search_fields = ('user_name',)

    @staticmethod
    def event_name(obj: ScanRecord):
        return obj.scan_event.name

    @staticmethod
    def user_name(obj: ScanRecord):
        return '{} {}'.format(
            obj.user_info.user.first_name,
            obj.user_info.user.last_name
        )
