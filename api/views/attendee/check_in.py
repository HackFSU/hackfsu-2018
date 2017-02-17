"""
    Check in an attendee
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import AttendeeStatus


class RequestForm(forms.Form):
    attendee_status_id = forms.IntegerField()


class CheckInView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])

    def work(self, request, req, res):
        attendee_info = AttendeeStatus.objects.filter(id=req['attendee_status_id'])

        if not attendee_info.exists():
            raise ValidationError('Invalid id', params=['attendee_status_id'])

        attendee_info = attendee_info[0]

        if attendee_info.checked_in_at is not None:
            raise ValidationError('Attendee already checked in', params=['attendee_status_id'])

        # Good, check them in
        attendee_info.checked_in_at = timezone.now()
        attendee_info.save()
