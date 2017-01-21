from django.db import models
from api.models import Hackathon


class ScheduleItem(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    start = models.DateTimeField()
    end = models.DateTimeField()
