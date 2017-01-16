"""
    User account registration. Creates basic user account
"""
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl


class RequestForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=100)
    password = forms.CharField(required=True, max_length=1000)


class ResponseForm(forms.Form):
    logged_in = forms.BooleanField()


class RegisterView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_deny=[acl.group_user])

    def work(self, request, req, res):
        # Attempt to create new user TODO

        # Send email for confirmation
        pass
