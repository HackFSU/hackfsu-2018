from django.db import models
from api.models import MentorInfo


class HelpRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    location = models.CharField(max_length=100)
    attendee_name = models.CharField(max_length=100)
    assigned_mentor = models.ForeignKey(to=MentorInfo, on_delete=models.SET_NULL, default=None, null=True, blank=True)

