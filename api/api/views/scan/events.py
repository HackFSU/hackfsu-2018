"""
    Get list of scan-events
"""

from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util.forms import JsonField
from hackfsu_com.util import acl
from api.models import ScanEvent, UserInfo

class ScanEventsView(ApiView):
    class ResponseForm(forms.Form):
        events = JsonField()

    http_method_names = ['get']
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])

    def work(self, request, req, res):
        scan_events = ScanEvent.objects.all()
        events_list = []

        for event in scan_events:
            events_list.append({
                'id': event.id,
                'name': event.name
            })

        res['events'] = events_list

class ScanUploadView(ApiView):
    class RequestForm(forms.Form):
        event = forms.IntegerField()
        hacker = forms.CharField()

    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])

    def work(self, request, req, res):

        # Identify which event we're scanning for
        event_id = req['event']
        event = ScanEvent.objects.get(id=event_id)

        # Check if this is the special-case check-in event
        # if event.is_check_in:
            # do check in things

        # Record hacker-scanevent relation
        hacker = UserInfo.objects.get(hexcode=req['hacker'])
        event.scanrecord_set.create(user_info=hacker)
