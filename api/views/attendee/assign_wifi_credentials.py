"""
    Sign in an attendee
"""

from django import forms
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl, email
from api.models import AttendeeStatus, WifiCred, Hackathon
import random


class RequestForm(forms.Form):
    attendee_status_id = forms.IntegerField()


class AssignWifiCredentialsView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])

    def work(self, request, req, res):
        attendee_info = AttendeeStatus.objects.filter(id=req['attendee_status_id'])

        if not attendee_info.exists():
            raise ValidationError('Invalid id', params=['attendee_status_id'])

        user = attendee_info[0].user

        if WifiCred.objects.filter(assigned_user=user).exists():
            raise ValidationError('Attendee already has wifi credentials', params=['attendee_status_id'])

        # Get new free wifi cred to assign
        credentials = WifiCred.objects.filter(hackathon=Hackathon.objects.current(), assigned_user__isnull=True)
        if not credentials.exists():
            raise ValidationError('No more wifi codes to assign!')

        credentials = credentials.all()
        cred = credentials[random.randint(0, len(credentials)-1)]

        # Assign
        cred.assigned_user = user
        cred.save()

        # Email
        email.send_template_to_user(user, 'wifi_credentials', 'Wifi Credentials', {
            'username': cred.username,
            'password': cred.password
        })

