"""
    Help request submission

    Protected by captcha.
"""

from django import forms
from hackfsu_com.util import captcha
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from api.models import HelpRequest, Hackathon


class RequestForm(forms.Form):
    g_recaptcha_response = forms.CharField(max_length=10000)
    location_x = forms.IntegerField(min_value=0, max_value=100)
    location_y = forms.IntegerField(min_value=0, max_value=100)
    location_floor = forms.IntegerField(min_value=1, max_value=3)
    attendee_name = forms.CharField(max_length=100)
    attendee_description = forms.CharField(max_length=100)
    request = forms.CharField(max_length=1000)


class CreateView(ApiView):
    request_form_class = RequestForm

    def authenticate(self, request):
        return super().authenticate(request) and Hackathon.objects.current().is_today()

    def work(self, request, req, res):
        # Check captcha
        if not captcha.is_valid_response(req['g_recaptcha_response']):
            raise ValidationError('Captcha check failed', params=['g_recaptcha_response'])

        HelpRequest.objects.create(
            hackathon=Hackathon.objects.current(),
            location_x=req['location_x'],
            location_y=req['location_y'],
            location_floor=req['location_floor'],
            attendee_name=req['attendee_name'],
            atendee_description=req['attendee_description'],
            request=req['request']
        )






