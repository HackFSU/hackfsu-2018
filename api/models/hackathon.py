from django.db import models
from django.contrib.postgres.fields import JSONField
from api import cache


class HackathonManager(models.Manager):
    def current(self):
        """ Selects the current hackathon. Will throw an error if no single current hackathons exist """
        return cache.get('HackathonManager.current_hackathon', self.get, current=True)


class Hackathon(models.Model):
    objects = HackathonManager()
    current = models.BooleanField(default=False)    # Only one should be current
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    statistics = JSONField(default=None, null=True, blank=True)    # Snapshot of info grabbed from db
    # mentors = 0
    # judges = 0
    # hackers_registered = 0
    # hackers_rsvp = 0
    # hackers_attended = 0
    # anon_stats = JSONField()
    # attendee_shirt_sizes = JSONField()

    def __str__(self):
        return self.name + (' [CURRENT]' if self.current else '')
