"""
    Hacker Registration
"""
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import HackerInfo


class RequestForm(forms.Form):
    is_first_hackathon = forms.BooleanField(required=True)
    is_adult = forms.BooleanField(required=True)
    agreed_to_mlh_data_sharing = forms.BooleanField(required=True)
    school_name = forms.CharField(required=True, max_length=100)  # Not final, may be id as well
    school_year = forms.ChoiceField(required=True, choices=HackerInfo.SCHOOL_YEAR_CHOICES)
    school_major = forms.CharField(required=True, max_length=100)   # Not final, may be id as well


class RegisterView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_user],
                                       acl_deny=[acl.group_hacker, acl.group_judge, acl.group_organizer])

    def work(self, request, req, res):
        # TODO
        pass
