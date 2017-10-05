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
    http_method_names = ['get']
    response_form_class = ResponseClass
    access_manager = acl.AccessManager(acl_accept=[acl.group_mentor])

    def work(self, request, req, res):
        help_requests = []
        for hr in HelpRequest.objects.filter(hackathon=Hackathon.objects.current()):
            help_requests.append(hr.json(request.user))

        res['help_requests'] = help_requests
