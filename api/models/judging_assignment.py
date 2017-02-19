from django.db import models
from api.models import Hackathon, Hack, JudgeInfo
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class JudgingAssignment(models.Model):
    STATUS_PENDING = 0
    STATUS_COMPLETE = 1
    STATUS_CANCELED = 2
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETE, 'Complete'),
        (STATUS_CANCELED, 'Canceled')
    )

    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    hack = models.ForeignKey(to=Hack, on_delete=models.CASCADE)
    judge = models.ForeignKey(to=JudgeInfo, on_delete=models.CASCADE),
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)


@admin.register(JudgingAssignment, site=hackfsu_admin)
class JudgingAssignmentAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'status')
    list_display = ('id', 'hack', 'judge', 'status')
    list_display_links = ('id',)
    list_editable = ('status',)
    search_fields = ('hack__name', 'hack__table_number', 'judge__user__first_name', 'judge__user__last_name')
    ordering = ('status',)
    actions = ('cancel',)

    def cancel(self, request, queryset):
        total = 0
        for assignment in queryset:
            assignment.status = JudgingAssignment.STATUS_CANCELED
            assignment.save()
            total += 1
        self.message_user(request, 'Canceled {} assignments(s)'.format(total))
    cancel.short_description = 'Cancel judging assignment'
