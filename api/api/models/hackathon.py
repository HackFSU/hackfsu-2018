from django.db import models
from django.contrib.postgres.fields import JSONField
from api import cache
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin
from django.utils import timezone


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
        if self.current:
            return '** {} **'.format(self.name)
        else:
            return self.name

    def is_today(self) -> bool:
        """
            Returns t/f based on if the hackathon is happening today
        """
        today = timezone.now().date()
        return (self.start_date <= today) and (today <= self.end_date)

    def is_over(self) -> bool:
        """
        :return: True if hackathon is over, false if upcoming/happening
        """
        today = timezone.now().date()
        return self.end_date < today


@admin.register(Hackathon, site=hackfsu_admin)
class HackathonAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('id', 'name', 'current', 'start_date', 'end_date')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('name',)
    ordering = ('-current', '-start_date')
