"""
    Retrieves basic user profile info
"""

from django import forms
from django.conf import settings
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from api.models import UserInfo, AttendeeStatus, Hackathon
import requests

class ProfileView(ApiView):

    class ResponseForm(forms.Form):
        first_name = forms.CharField()
        last_name = forms.CharField()
        email = forms.CharField()
        groups = JsonField()
        shirt_size = forms.CharField()
        phone_number = forms.CharField()
        diet = forms.CharField(required=False)
        github = forms.CharField(required=False)
        linkedin = forms.CharField(required=False)
        rsvp_confirmed = forms.BooleanField(required=False)
        checked_in = forms.BooleanField(required=False)

    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_user])
    response_form_class = ResponseForm

    def work(self, request, req, res):
        # Base info
        res['first_name'] = request.user.first_name
        res['last_name'] = request.user.last_name
        res['email'] = request.user.email
        res['groups'] = list(request.user.groups.values_list('name', flat=True))

        # Extra info
        user_info = UserInfo.objects.get(user=request.user)
        res['shirt_size'] = user_info.shirt_size
        res['github'] = user_info.github
        res['linkedin'] = user_info.linkedin
        res['phone_number'] = user_info.phone_number
        res['diet'] = user_info.diet

        # Attendee Status info
        res['rsvp_confirmed'] = AttendeeStatus.objects.filter(
            hackathon=Hackathon.objects.current(), user=request.user, rsvp_submitted_at__isnull=False
        ).exists()
        res['checked_in'] = AttendeeStatus.objects.filter(
            hackathon=Hackathon.objects.current(), user=request.user, checked_in_at__isnull=False
        ).exists()


class HexCodeView(ProfileView):

    class ResponseForm(forms.Form):
        hexcode = forms.CharField(required=True)

    response_form_class = ResponseForm

    def work(self, request, req, res):
        user_info = UserInfo.objects.get(user=request.user)

        code = user_info.hexcode or None

        if not code:
            url = "http://{}/hex/{}".format(settings.QR_HOST, request.user.email)
            resp = requests.get(url)

            if resp.status_code in (200, 201):
                code = str(resp.json().get('code'))

                if user_info.hexcode is None:
                    user_info.hexcode = code
                    user_info.save()
            else:
                raise ValueError('Could not get key for {}'.format(request.user.email))

        res['hexcode'] = code
