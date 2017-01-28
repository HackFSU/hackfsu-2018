from django.db import models
from api.models import Hackathon


class HackathonMap(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    order = models.SmallIntegerField()

    def __str__(self):
        return 'hackathon={} title="{}" order={} link="{}"' .format(
            self.hackathon.id,
            self.title,
            self.order,
            self.link
        )
