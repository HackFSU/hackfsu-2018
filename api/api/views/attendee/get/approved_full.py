"""
    Retrieves all the attendees with their groups, statuses, and user information
"""

from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from api.models import AttendeeStatus, Hackathon
from django.db.models import Q


class RequestForm(forms.Form):
    draw = forms.IntegerField()
    start = forms.IntegerField()
    length = forms.IntegerField()


class ResponseForm(forms.Form):
    draw = forms.IntegerField()
    recordsTotal = forms.IntegerField()
    recordsFiltered = forms.IntegerField()
    data = JsonField()


class ApprovedFullView(ApiView):
    http_method_names = ['get']
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])

    GET_PARAM_SEARCH = 'search[value]'

    def work(self, request, req, res):
        attendees = []
        statuses = AttendeeStatus.objects.filter(
                hackathon=Hackathon.objects.current(),
                user__groups__name__in=[
                    acl.group_hacker,
                    acl.group_mentor,
                    acl.group_judge,
                    acl.group_organizer
                ],

        ).order_by('user__first_name', 'user__last_name').distinct()

        res['recordsTotal'] = statuses.count()

        # Apply search filter
        filtered_statuses = statuses
        if self.GET_PARAM_SEARCH in request.GET:
            search = request.GET[self.GET_PARAM_SEARCH]
            if len(search) > 3:
                filtered_statuses = statuses.filter(
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search) |
                    Q(user__email__icontains=search)
                )
        res['recordsFiltered'] = filtered_statuses.count()

        offset = req['start']
        limit = offset + req['length']
        returned_statuses = filtered_statuses.all()[offset:limit]

        for status in returned_statuses:
            attendee = {
                'groups': list(status.user.groups.filter(name__in=[
                    acl.group_hacker,
                    acl.group_mentor,
                    acl.group_judge,
                    acl.group_organizer
                ]).all().values_list('name', flat=True))
            }

            if len(attendee['groups']) > 0:
                attendee['id'] = status.id
                attendee['name'] = '{} {}'.format(status.user.first_name, status.user.last_name)
                attendee['email'] = status.user.email
                attendee['checked_in'] = status.checked_in_at is not None
                attendee['has_wifi_credentials'] = hasattr(status.user, 'wificred')
                attendees.append(attendee)

        res['data'] = attendees
        res['draw'] = req['draw']
