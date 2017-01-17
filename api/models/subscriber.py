from django.db import models
from api.models import Hackathon


class Subscriber(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return 'id={}, hackathon.name={}, email={}'.format(
            self.id, str(self.hackathon), self.email
        )
