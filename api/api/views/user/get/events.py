"""
    Retrieves list of events for a user_info
"""

from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util.forms import JsonField
from hackfsu_com.util import acl
from api.models import ScanRecord, UserInfo

class EventsView(ApiView):
    class ResponseForm(forms.Form):
        events = JsonField()

    http_method_names = ['get']
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_user])

    def work(self, request, req, res):
        user_info = UserInfo.objects.get(user=request.user)
        scan_records = ScanRecord.objects.filter(user_info=user_info)
        records_list = []

        for record in scan_records:
            records_list.append({
                'time': record.time.isoformat(),
                'name': record.scan_event.name
            })

        res['events'] = records_list
