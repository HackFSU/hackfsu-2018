"""
    Get list of countdowns for current hackathon
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import ApiView
from api.models import Hackathon, HackathonMap


class ResponseForm(forms.Form):
    maps = forms.Field()


class MapsView(ApiView):
    response_form_class = ResponseForm

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        maps = HackathonMap.objects.filter(hackathon=current_hackathon)

        maps_list = []
        for hackathon_map in maps:
            maps_list.append({
                'title': hackathon_map.title,
                'link': hackathon_map.link,
                'order': hackathon_map.order
            })

        res['maps'] = maps_list
