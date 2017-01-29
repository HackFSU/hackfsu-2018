from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from hackfsu_com.util import acl
from api.models import Hackathon
from django.contrib import admin


class AttendeeStatusManager(models.Manager):
    @staticmethod
    def get_or_create(user: User, hackathon: Hackathon):
        """ Gets current attendee status for user/hackathon combo. If non exists one is created properly """
        try:
            attendee_status = AttendeeStatus.objects.get(user=user, hackathon=hackathon)
        except ObjectDoesNotExist:
            attendee_status = AttendeeStatus.objects.create(user=user, hackathon=hackathon)
            acl.add_user_to_group(user, acl.group_attendee)
        return attendee_status


class AttendeeStatus(models.Model):
    objects = AttendeeStatusManager()

    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    comments = models.CharField(max_length=1000, default='')
    rsvp_email_sent = models.BooleanField(default=False)
    rsvp_email_sent_timestamp = models.DateTimeField(null=True)
    rsvp_confirmed = models.BooleanField(default=False)
    rsvp_confirmed_timestamp = models.DateTimeField(null=True)
    checked_in = models.BooleanField(default=False)
    checked_in_timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return '[{} {}\'s Attendee Status]'.format(self.user.first_name, self.user.last_name)


@receiver(pre_delete, sender=AttendeeStatus)
def on_pre_delete(**kwargs):
    """ Update base user class's groups """
    instance = kwargs['instance']
    if instance.hackathon == Hackathon.objects.current():
        acl.remove_user_from_group(instance.user, acl.group_attendee)


@admin.register(AttendeeStatus)
class AttendeeStatusAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'rsvp_email_sent', 'rsvp_confirmed', 'checked_in')
    list_display = ('id', 'user', 'created', 'comments')
    list_editable = ('comments',)
    list_display_links = ('id',)
    search_fields = ('user', 'comments')
    ordering = ('-created',)
