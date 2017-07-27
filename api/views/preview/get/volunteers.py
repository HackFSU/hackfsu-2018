"""
    Retrieves list of all volunteer prereg emails.
"""

from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from api.models import PreviewEmail

class ResponseForm(forms.Form):
    emails = JsonField()

class VolunteersView(ApiView):
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
    response_form_class = ResponseForm

    def work(self, request, req, res):
        prereqs = PreviewEmail.objects.filter(interest='volunteer')
        emails  = set([prereq.email for prereq in prereqs])

        res['emails'] = list(emails)
