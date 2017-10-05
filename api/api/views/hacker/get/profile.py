
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl, files
from api.models import Hackathon, HackerInfo


class ResponseForm(forms.Form):
    approved = forms.BooleanField(required=False)
    is_first_hackathon = forms.BooleanField(required=False)
    is_adult = forms.BooleanField(required=False)
    school = forms.CharField(required=False)
    school_year = forms.CharField(required=False)
    school_major = forms.CharField(required=False)
    resume_url = forms.CharField(required=False)
    interests = forms.CharField(required=False)


class ProfileView(ApiView):
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_hacker, acl.group_pending_hacker])
    response_form_class = ResponseForm

    def work(self, request, req, res):
        current_hackathon = Hackathon.objects.current()
        hacker_info = HackerInfo.objects.get(hackathon=current_hackathon, user=request.user)

        # Status flags
        res['approved'] = hacker_info.approved

        # Entered data
        res['is_first_hackathon'] = hacker_info.is_first_hackathon
        res['is_adult'] = hacker_info.is_adult
        res['school'] = hacker_info.school.name
        res['school_year'] = hacker_info.school_year
        res['school_major'] = hacker_info.school_major
        res['interests'] = hacker_info.interests

        if len(hacker_info.resume_file_name) > 0:
            res['resume_url'] = files.get_url(hacker_info.resume_file_name)
