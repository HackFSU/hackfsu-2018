"""
    Get list of countdowns for current hackathon
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import PublicApiView
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, ScheduleItem


class ResponseForm(forms.Form):
    schedule_items = JsonField()


class ScheduleItemsView(PublicApiView):
    response_form_class = ResponseForm

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        items = ScheduleItem.objects.filter(hackathon=current_hackathon).order_by('start', 'end')

        items_list = []
        for item in items:
            item_data = {
                'name': item.name,
                'description': item.description,
                'start': item.start.isoformat(),
                'type': item.type
            }

            if item.end is not None:
                item_data['end'] = item.end.isoformat()

            items_list.append(item_data)

        res['schedule_items'] = items_list
