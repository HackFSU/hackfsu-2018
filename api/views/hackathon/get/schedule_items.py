"""
    Get list of countdowns for current hackathon
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import ApiView
from api.models import Hackathon, ScheduleItem


class ResponseForm(forms.Form):
    schedule_items = forms.Field()


class ScheduleItemsView(ApiView):
    response_form_class = ResponseForm

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        items = ScheduleItem.objects.filter(hackathon=current_hackathon)

        items_list = []
        for item in items:
            items_list.append({
                'name': item.name,
                'description': item.description,
                'start': item.start.isoformat(),
                'end': item.end.isoformat()
            })

        res['schedule_items'] = items_list
