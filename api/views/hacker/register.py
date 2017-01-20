"""
    Hacker Registration
"""
from django import forms
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import HackerInfo


class RequestForm(forms.Form):
    is_first_hackathon = forms.BooleanField(required=True)
    is_adult = forms.BooleanField()
    school_name = forms.CharField(required=True, max_length=100)  # Not final, may be id as well
    school_year = forms.ChoiceField(required=True, choices=HackerInfo.SCHOOL_YEAR_CHOICES)
    school_major = forms.CharField(required=True, max_length=100)   # Not final, may be id as well


class RegisterView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_user],
                                       acl_deny=[acl.group_hacker, acl.group_judge, acl.group_organizer,
                                                 acl.group_pending_hacker, acl.group_pending_judge,
                                                 acl.group_pending_organizer])

    def work(self, request, req, res):
        # Create HackerInfo TODO

        # Add to user group TODO
        pass

