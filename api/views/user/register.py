"""
    User account registration. Creates basic user account
"""
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import UserInfo


class RequestForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=100)
    password = forms.CharField(required=True, max_length=1000)
    github = forms.CharField(max_length=100)
    diet = forms.CharField(max_length=500)
    shirt_size = forms.ChoiceField(choices=UserInfo.SHIRT_SIZE_CHOICES)
    phone_number = forms.CharField(max_length=20)
    # TODO agree to terms of service (bool)
    # TODO agree to MLH code of conduct (bool)


class RegisterView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_deny=[acl.group_user])

    def work(self, request, req, res):
        # Attempt to create new user TODO

        # Send email for confirmation
        pass
