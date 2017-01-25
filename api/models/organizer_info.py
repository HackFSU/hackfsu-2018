from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from api.models import Hackathon
from hackfsu_com.util import acl


class OrganizerInfo(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    comments = models.CharField(max_length=1000, default='', blank=True)
    misc_info = JSONField(default=None, null=True, blank=True)

    affiliation = models.CharField(max_length=100)


@receiver(pre_delete, sender=OrganizerInfo)
def on_pre_delete(**kwargs):
    """ Update base user class's groups """
    instance = kwargs['instance']
    if instance.hackathon == Hackathon.objects.current():
        acl.remove_user_from_groups(instance.user, [acl.group_organizer, acl.group_pending_organizer])
