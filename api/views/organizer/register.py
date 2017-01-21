"""
    Organizer registration
"""
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl


class RequestForm(forms.Form):
    affiliation = forms.CharField(required=True, max_length=100)
    # TODO agree to not give out personal info
    # TODO other info maybe


class RegisterView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_user],
                                       acl_deny=[acl.group_hacker, acl.group_organizer,
                                                 acl.group_pending_hacker, acl.group_pending_organizer])

    def work(self, request, req, res):
        # TODO
        pass