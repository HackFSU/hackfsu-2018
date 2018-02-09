"""
    Submit an RSVP for the current user
"""

from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import AttendeeStatus, Hackathon
from django.utils import timezone


class RequestForm(forms.Form):
    rsvp_answer = forms.BooleanField(required=False)
    extra_info = forms.CharField(required=False, max_length=500)


class RsvpView(ApiView):
    request_form_class = RequestForm
    allowed_after_current_hackathon_ends = True
    access_manager = acl.AccessManager(acl_accept=[
        acl.group_hacker,
        acl.group_mentor,
        acl.group_organizer,
        acl.group_judge
    ])

    def authenticate(self, request):
        if not super().authenticate(request):
            return False

        # Add check to make sure not already RSVP'd
        return AttendeeStatus.objects.filter(
            hackathon=Hackathon.objects.current(), user=request.user, rsvp_submitted_at__isnull=True
        ).exists()

    def work(self, request, req, res):

        status = AttendeeStatus.objects.get(hackathon=Hackathon.objects.current(), user=request.user)

        status.rsvp_result = req['rsvp_answer']
        status.rsvp_submitted_at = timezone.now()
        status.extra_info = req['extra_info']
        status.save()

