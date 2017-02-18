"""
    Gets all listed prizes for hackathon
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import PublicApiView
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, HackathonPrize


class ResponseForm(forms.Form):
    prizes = JsonField()


class PrizesView(PublicApiView):
    response_form_class = ResponseForm

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        prizes = HackathonPrize.objects.filter(hackathon=current_hackathon).order_by('award_giver')

        prize_list = []
        for prize in prizes:
            prize_list.append({
                'award_giver': prize.award_giver,
                'title': prize.title,
                'description': prize.description
            })

        res['prizes'] = prize_list
