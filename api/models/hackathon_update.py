from django.db import models
from api.models import Hackathon


class HackathonUpdate(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    submit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'hackathon={} submit_time={} title="{}" content="{}"'.format(
            self.hackathon.id,
            self.submit_time,
            self.title,
            self.content
        )
