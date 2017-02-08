from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from api.models import Hackathon, AttendeeStatus
from hackfsu_com.util import acl
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class OrganizerInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    attendee_status = models.OneToOneField(to=AttendeeStatus, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    affiliation = models.CharField(max_length=100)
    teams = models.CharField(max_length=100)
    motivation = models.CharField(max_length=1000)

    def __str__(self):
        return '[Organizer {} {}]'.format(self.user.first_name, self.user.last_name)


@receiver(pre_delete, sender=OrganizerInfo)
def on_pre_delete(**kwargs):
    """ Update base user class's groups """
    instance = kwargs['instance']
    if instance.hackathon == Hackathon.objects.current():
        acl.remove_user_from_groups(instance.user, [acl.group_organizer, acl.group_pending_organizer])


@admin.register(OrganizerInfo, site=hackfsu_admin)
class OrganizerInfoAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'approved')
    list_display = ('id', 'user_info', 'approved', 'teams', 'affiliation', 'motivation', 'created')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'affiliation', 'teams', 'motivation')
    ordering = ('-created',)

    @staticmethod
    def user_info(obj):
        return "{} {} - {}".format(obj.user.first_name, obj.user.last_name, obj.user.email)
