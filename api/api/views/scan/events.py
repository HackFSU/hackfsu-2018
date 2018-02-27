"""
    Get list of scan-events
"""

from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util.forms import JsonField
from hackfsu_com.util import acl
from api.models import Hackathon, ScanEvent, ScanRecord, UserInfo, HackerInfo
from api.models.attendee_status import AttendeeStatusManager

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

    class ResponseForm(forms.Form):
        message = forms.CharField()
        status = forms.IntegerField()
        name = forms.CharField(required=False)

    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])

    def work(self, request, req, res):

        # Make sure we recognize user
        try:
            hacker = UserInfo.objects.get(hexcode=req['hacker'])
            user = User.objects.get(userinfo=hacker)
            name = user.first_name + ' ' + user.last_name
        except:
            res['message'] = "User with hexcode {} not found.".format(req['hacker'])
            res['status'] = 404
            return

        # Identify which event we're scanning for
        event_id = req['event']
        event = ScanEvent.objects.get(id=event_id)

        # Check if record for event-hacker already exists
        records = ScanRecord.objects.filter(user_info=hacker, scan_event=event)

        # If record already exists, they did this already
        if len(records) > 0:
            res['name'] = name
            res['message'] = "{} already did this event.".format(name)
            res['status'] = 401
            return

        # Check if this is the special-case check-in event
        if event.is_check_in:
            current_hackathon = Hackathon.objects.current()
            attendee_info = AttendeeStatusManager.get_or_create(user, current_hackathon)

            # If hacker, make sure they are approved
            try:
                hacker_info = HackerInfo.objects.get(hackathon=current_hackathon, user=user)
                if not hacker_info.approved:
                    res['name'] = name
                    res['message'] = "{} was not accepted.".format(name)
                    res['status'] = 401
                    return
            except:
                pass


            attendee_info.checked_in_at = timezone.now()
            attendee_info.save()


        # Record hacker-scanevent relation
        event.scanrecord_set.create(user_info=hacker)

        res['name'] = name
        res['message'] = "Scan OK!"
        res['status'] = 200

