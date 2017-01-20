"""
    Judge registration
"""
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl


class RequestForm(forms.Form):
    affiliation = forms.CharField(max_length=100)
    # TODO other info maybe


class RegisterView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_user],
                                       acl_deny=[acl.group_hacker, acl.group_judge, acl.group_pending_judge,
                                                 acl.group_pending_hacker])

    def work(self, request, req, res):
        # TODO
        pass
