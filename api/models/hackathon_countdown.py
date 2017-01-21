from django.db import models
from api.models import Hackathon


class HackathonCountdown(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()
