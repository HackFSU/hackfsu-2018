from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib import admin
from api.models import Hackathon, School, AttendeeStatus
from hackfsu_com.util import acl, files


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
    attendee_status = models.OneToOneField(to=AttendeeStatus, on_delete=models.CASCADE, null=True)  # TODO null=False
    approved = models.BooleanField(default=False, blank=True)
    is_first_hackathon = models.BooleanField()
    is_adult = models.BooleanField()
    school = models.ForeignKey(to=School, on_delete=models.SET_NULL, null=True)
    school_year = models.CharField(max_length=2, choices=SCHOOL_YEAR_CHOICES)
    school_major = models.CharField(max_length=100)
    resume_file_name = models.CharField(max_length=300, default='', blank=True)
    interests = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        summary = 'email="{}" name="{} {}" approved={}'.format(
            self.user.email,
            self.user.first_name, self.user.last_name,
            self.approved
        )

        return summary


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


@admin.register(HackerInfo)
class HackerAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'approved', 'is_first_hackathon', 'is_adult', 'school_year')
