"""
    Judge registration
"""
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl, email
from api.models import JudgeInfo, Hackathon, AttendeeStatus


class RequestForm(forms.Form):
    affiliation = forms.CharField(max_length=100)
    organizer_contact = forms.CharField(max_length=100)


class RegisterView(ApiView):
    request_form_class = RequestForm
    allowed_after_current_hackathon_ends = False
    access_manager = acl.AccessManager(acl_accept=[acl.group_user],
                                       acl_deny=[acl.group_hacker, acl.group_judge, acl.group_pending_judge,
                                                 acl.group_pending_hacker])

    def work(self, request, req, res):
        # Ensure is attendee
        current_hackathon = Hackathon.objects.current()
        attendee_status = AttendeeStatus.objects.get_or_create(user=request.user, hackathon=current_hackathon)

        JudgeInfo.objects.create(
            hackathon=current_hackathon,
            user=request.user,
            attendee_status=attendee_status,
            affiliation=req['affiliation'],
            organizer_contact=req['organizer_contact']
        )

        acl.add_user_to_group(request.user, acl.group_pending_judge)

        # Send email for confirmation
        email.send_template(
            to_email=request.user.email,
            to_first_name=request.user.first_name,
            to_last_name=request.user.last_name,
            subject='Judge Registration Submitted!',
            template_name='judge_register_waiting'
        )

