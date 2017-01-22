
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl, files
from api.models import Hackathon, HackerInfo


class ResponseForm(forms.Form):
    approved = forms.BooleanField()
    is_first_hackathon = forms.BooleanField()
    is_adult = forms.BooleanField()
    school_id = forms.IntegerField()
    school_year = forms.CharField()
    school_major = forms.CharField()
    resume_url = forms.CharField()
    checked_in = forms.BooleanField()
    rsvp = forms.BooleanField()


class ProfileView(ApiView):
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_hacker, acl.group_pending_hacker])
    response_form_class = ResponseForm

    def work(self, request, req, res):
        current_hackathon = Hackathon.objects.current()
        hacker_info = HackerInfo.objects.get(hackathon=current_hackathon, user=request.user)

        # Status flags
        req['approved'] = hacker_info.approved
        req['checked_in'] = hacker_info.checked_in
        req['rsvp'] = hacker_info.rsvp

        # Entered data
        req['is_first_hackathon'] = hacker_info.is_first_hackathon
        req['is_adult'] = hacker_info.is_adult
        req['school_id'] = hacker_info.school_id
        req['school_year'] = hacker_info.school_year
        req['school_major'] = hacker_info.school_major

        if len(hacker_info.resume_file_name) > 0:
            req['resume_url'] = files.get_url(hacker_info.resume_file_name)
