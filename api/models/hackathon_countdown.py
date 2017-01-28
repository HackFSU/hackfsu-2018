from django.db import models
from api.models import Hackathon


class HackathonCountdown(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return 'hackathon={} title="{}" start={} end={}'.format(
            self.hackathon.id,
            self.title,
            self.start,
            self.end
        )

