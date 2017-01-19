from django.db import models
from django.contrib.auth.models import User
from api.models import Hackathon


class HackerInfo(models.Model):
    SCHOOL_YEAR_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    is_first_hackathon = models.BooleanField()
    is_adult = models.BooleanField()
    school_name = models.CharField(max_length=100)
    school_year = models.CharField(max_length=2, choices=SCHOOL_YEAR_CHOICES)
    school_major = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    rsvp = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)
    comments = models.CharField(max_length=1000, default='', blank=True)
