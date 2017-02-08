from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from api.models import Hackathon, AttendeeStatus
from hackfsu_com.util import acl, email
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class JudgeInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    attendee_status = models.OneToOneField(to=AttendeeStatus, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    affiliation = models.CharField(max_length=100)
    organizer_contact = models.CharField(max_length=100)

    def __str__(self):
        return '[JudgeInfo {} {}]'.format(self.user.first_name, self.user.last_name)


@receiver(pre_delete, sender=JudgeInfo)
def on_pre_delete(**kwargs):
    """ Update base user class's groups """
    instance = kwargs['instance']
    if instance.hackathon == Hackathon.objects.current():
        acl.remove_user_from_groups(instance.user, [acl.group_judge, acl.group_pending_judge])


@admin.register(JudgeInfo, site=hackfsu_admin)
class JudgeInfoAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'approved')
    list_display = ('id', 'user_info', 'approved', 'affiliation', 'organizer_contact', 'created')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'affiliation', 'organizer_contact')
    ordering = ('-created',)
    # actions = ('approve_application', 'un_approve_application')

    @staticmethod
    def user_info(obj):
        return "{} {} - {}".format(obj.user.first_name, obj.user.last_name, obj.user.email)

    def approve_application(self, request, queryset):
        total = 0
        for obj in queryset:
            if obj.approved is False:
                acl.add_user_to_group(obj.user, acl.group_judge)
                acl.remove_user_from_group(obj.user, acl.group_pending_judge)
                obj.approved = True
                obj.save()
                total += 1
                email.send_template_to_user(
                    obj.user, 'judge_register_accepted', 'HackFSU Judge Registration Approved'
                )
        self.message_user(request, 'Approved & emailed {} pending judges'.format(total))
    approve_application.short_description = 'Approve pending-judge'

    def un_approve_application(self, request, queryset):
        total = 0
        for obj in queryset:
            if obj.approved is True:
                acl.remove_user_from_group(obj.user, acl.group_judge)
                acl.add_user_to_group(obj.user, acl.group_pending_judge)
                obj.approved = False
                obj.save()
                total += 1
        self.message_user(request, 'Un-approved {} judges'.format(total))
    un_approve_application.short_description = 'Un-Approve judge'
