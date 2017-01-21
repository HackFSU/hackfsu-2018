"""
    Get list of countdowns for current hackathon
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, HackathonCountdown


class ResponseForm(forms.Form):
    countdowns = JsonField()


class CountdownsView(ApiView):
    response_form_class = ResponseForm

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        countdowns = HackathonCountdown.objects.filter(hackathon=current_hackathon)

        countdown_list = []
        for cd in countdowns:
            countdown_list.append({
                'title': cd.title,
                'start': cd.start.isoformat(),
                'end': cd.end.isoformat()
            })

        res['countdowns'] = countdown_list
