from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib import admin
from api.models import Hackathon, School, AttendeeStatus
from hackfsu_com.util import acl, files, email
from hackfsu_com.admin import hackfsu_admin


class HackerInfo(models.Model):
    SCHOOL_YEAR_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('SS', 'Super Senior'),
        ('GS', 'Graduate Student'),
        ('HS', 'High School Student'),
        ('RG', 'Recent College Graduate')
    )
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    attendee_status = models.OneToOneField(to=AttendeeStatus, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False, blank=True)
    is_first_hackathon = models.BooleanField()
    is_adult = models.BooleanField()
    school = models.ForeignKey(to=School, on_delete=models.SET_NULL, null=True)
    school_year = models.CharField(max_length=2, choices=SCHOOL_YEAR_CHOICES)
    school_major = models.CharField(max_length=100)
    resume_file_name = models.CharField(max_length=300, default='', blank=True)
    interests = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        return '[HackerInfo {} {}]'.format(self.user.first_name, self.user.last_name)


@receiver(pre_delete, sender=HackerInfo)
def on_pre_delete(**kwargs):
    """ Delete cleanup """
    instance = kwargs['instance']

    # Update base user class's groups
    if instance.hackathon == Hackathon.objects.current():
        acl.remove_user_from_groups(instance.user, [acl.group_hacker, acl.group_pending_hacker])

    # Delete stored resume file
    if len(instance.resume_file_name) > 0:
        files.delete_if_exists(instance.resume_file_name)


@admin.register(HackerInfo, site=hackfsu_admin)
class HackerAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'approved', 'is_first_hackathon', 'is_adult', 'school_year')
    list_display = ('id', 'user_info', 'attendee_status', 'approved', 'school', 'school_year', 'school_major',
                    'is_first_hackathon', 'is_adult', 'interests', 'resume_file_name', 'created')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'school__name')
    ordering = ('-created',)
    # actions = ('approve_application', 'un_approve_application')

    @staticmethod
    def user_info(obj):
        return "{} {} - {}".format(obj.user.first_name, obj.user.last_name, obj.user.email)

    def approve_application(self, request, queryset):
        total = 0
        for obj in queryset:
            if obj.approved is False:
                acl.add_user_to_group(obj.user, acl.group_hacker)
                acl.remove_user_from_group(obj.user, acl.group_pending_hacker)
                obj.approved = True
                obj.save()
                total += 1
                email.send_template_to_user(
                    obj.user, 'hacker_register_accepted', 'HackFSU Hacker Registration Approved'
                )
        self.message_user(request, 'Approved & emailed {} pending hackers'.format(total))
    approve_application.short_description = 'Approve pending-hacker'

    def un_approve_application(self, request, queryset):
        total = 0
        for obj in queryset:
            if obj.approved is True:
                acl.remove_user_from_group(obj.user, acl.group_hacker)
                acl.add_user_to_group(obj.user, acl.group_pending_hacker)
                obj.approved = False
                obj.save()
                total += 1
        self.message_user(request, 'Un-approved {} hackers'.format(total))
    un_approve_application.short_description = 'Un-Approve hacker'
