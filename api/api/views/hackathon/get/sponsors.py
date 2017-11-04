"""
    Get list of countdowns for current hackathon

    Will only return sponsors for app unless all=True
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import PublicApiView
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, HackathonSponsor


class RequestForm(forms.Form):
    all = forms.BooleanField(required=False)


class ResponseForm(forms.Form):
    sponsors = JsonField()


class SponsorsView(PublicApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        sponsors = HackathonSponsor.objects.filter(hackathon=current_hackathon)

        if not req['all']:
            sponsors = sponsors.filter(on_mobile=True)

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
