
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import Hackathon, MentorInfo


class ResponseForm(forms.Form):
    approved = forms.BooleanField()
    checked_in = forms.BooleanField()
    rsvp = forms.BooleanField()

    affiliation = forms.CharField()


class ProfileView(ApiView):
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_mentor, acl.group_pending_mentor])
    response_form_class = ResponseForm

    def work(self, request, req, res):
        current_hackathon = Hackathon.objects.current()
        info = MentorInfo.objects.get(hackathon=current_hackathon, user=request.user)

        # Status flags
        req['approved'] = info.approved
        req['checked_in'] = info.checked_in
        req['rsvp'] = info.rsvp

        # Entered data
        res['affiliation'] = info.affiliation
