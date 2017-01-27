from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from hackfsu_com.util import acl
from api.models import Hackathon


class AttendeeStatus(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    comments = models.CharField(max_length=1000, default='')
    rsvp_email_sent = models.BooleanField(default=False)
    rsvp_confirmed = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)


@receiver(pre_delete, sender=AttendeeStatus)
def on_pre_delete(**kwargs):
    """ Update base user class's groups """
    instance = kwargs['instance']
    if instance.hackathon == Hackathon.objects.current():
        acl.remove_user_from_groups(instance.user, [acl.group_attendee])
