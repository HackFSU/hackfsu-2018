"""
    Retrieves just the current user's groups
"""

from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField


class ResponseForm(forms.Form):
    groups = JsonField()


class GroupsView(ApiView):
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_user])
    response_form_class = ResponseForm

    def work(self, request, req, res):
        res['groups'] = list(request.user.groups.values_list('name', flat=True))
