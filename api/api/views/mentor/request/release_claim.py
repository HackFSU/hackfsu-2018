"""
    Un-claims a help request. Can only be done by mentors.
"""

from django import forms
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import HelpRequest, MentorInfo


class RequestForm(forms.Form):
    help_request_id = forms.IntegerField()


class ReleaseClaimView(ApiView):
    allowed_after_current_hackathon_ends = False
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_mentor])

    def work(self, request, req, res):
        help_request = HelpRequest.objects.filter(id=req['help_request_id'])
        if help_request.exists():
            help_request = help_request[0]
        else:
            raise ValidationError('Invalid help request id')

        if help_request.assigned_mentor is None \
                or help_request.assigned_mentor != MentorInfo.objects.get(user=request.user):
            raise ValidationError('You may only un-claim your own claimed requests')

        # Remove claim
        help_request.assigned_mentor = None
        help_request.save()
