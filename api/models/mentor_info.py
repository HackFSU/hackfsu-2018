from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from api.models import Hackathon


class MentorInfo(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    comments = models.CharField(max_length=1000, default='', blank=True)
    misc_info = JSONField(default=None, null=True, blank=True)

    affiliation = models.CharField(max_length=100)
