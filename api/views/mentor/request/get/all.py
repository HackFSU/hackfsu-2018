"""
    Retrieves all requests for the current hackathon
"""

from django import forms
from hackfsu_com.util.forms import JsonField
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import HelpRequest, Hackathon


class ResponseClass(forms.Form):
    help_requests = JsonField()


class AllView(ApiView):
    http_method_names = ['GET']
    response_form_class = ResponseClass
    access_manager = acl.AccessManager(acl_accept=[acl.group_mentor])

    def work(self, request, req, res):
        help_requests = []
        for request in HelpRequest.objects.filter(hackathon=Hackathon.objects.current()):
            r = {
                'id': request.id,
                'location': {
                    'floor': request.location_floor,
                    'x': request.location_x,
                    'y': request.location_y
                },
                'attendee': {
                    'name': request.attendee_name,
                    'description': request.attendee_description
                },
                'request': request.request
            }
            if hasattr(request, 'assigned_mentor'):
                user = request.assigned_mentor.user
                r['assigned_mentor'] = {
                    'name': '{} {}'.format(user.first_name, user.last_name),
                    'is_me': request.user.id == user.id
                }

            help_requests.append(r)

        res['help_requests'] = help_requests
