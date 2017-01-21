"""
    Get list of countdowns for current hackathon
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, HackathonSponsor


class ResponseForm(forms.Form):
    sponsors = JsonField()


class SponsorsView(ApiView):
    response_form_class = ResponseForm

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        sponsors = HackathonSponsor.objects.filter(hackathon=current_hackathon)

        sponsors_list = []
        for sponsor in sponsors:
            sponsors_list.append({
                'name': sponsor.name,
                'website_link': sponsor.website_link,
                'logo_link': sponsor.logo_link,
                'tier': sponsor.tier,
                'order': sponsor.order
            })

        res['sponsors'] = sponsors_list
