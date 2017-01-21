from django.db import models
from api.models import Hackathon


class HackathonSponsor(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    website_link = models.CharField(max_length=500)
    logo_link = models.CharField(max_length=500)
    tier = models.SmallIntegerField(default=0)
    order = models.SmallIntegerField(default=0)
