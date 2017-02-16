"""
    Retrieves a single help request by id
"""

from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from hackfsu_com.util.forms import JsonField
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import HelpRequest, Hackathon


class ResponseClass(forms.Form):
    help_request = JsonField()


class SingleView(ApiView):
    http_method_names = ['get']
    response_form_class = ResponseClass
    access_manager = acl.AccessManager(acl_accept=[acl.group_mentor])

    def work(self, request, req, res):
        try:
            help_request = HelpRequest.objects.get(id=self.kwargs['id'])
        except ObjectDoesNotExist:
            raise ValidationError('Invalid id', params=['id'])

        res['help_request'] = help_request.json(request.user)
