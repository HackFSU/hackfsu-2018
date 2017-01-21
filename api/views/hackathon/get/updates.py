"""
    Get list of countdowns for current hackathon
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import PublicApiView
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, HackathonUpdate


class ResponseForm(forms.Form):
    updates = JsonField()


class UpdatesView(PublicApiView):
    response_form_class = ResponseForm

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        updates = HackathonUpdate.objects.filter(hackathon=current_hackathon)

        updates_list = []
        for update in updates:
            updates_list.append({
                'title': update.title,
                'content': update.content,
                'submit_time': update.submit_time.isoformat()
            })

        res['updates'] = updates_list
