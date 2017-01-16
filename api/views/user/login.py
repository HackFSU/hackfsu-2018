"""
    Logs user with the given credentials in for the stored session
"""
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl


class RequestForm(forms.Form):
    email = forms.EmailField(required=True, max_length=100)
    password = forms.CharField(required=True, max_length=1000)


class LogInView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_deny=[acl.group_user])

    def work(self, request, req, res):
        # Authenticate user (username == email)
        user = authenticate(
            username=req['email'],
            password=req['password']
        )
        if user is None:
            raise ValidationError(_('Invalid email or password'))
        login(request, user)
