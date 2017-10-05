"""
    Organizer registration
"""
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl, email
from api.models import OrganizerInfo, Hackathon, AttendeeStatus


class RequestForm(forms.Form):
    agree_to_terms = forms.BooleanField()
    affiliation = forms.CharField( max_length=100)
    teams = forms.CharField(max_length=100)
    motivation = forms.CharField(max_length=1000)


class RegisterView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_user],
                                       acl_deny=[acl.group_hacker, acl.group_organizer,
                                                 acl.group_pending_hacker, acl.group_pending_organizer])

    def work(self, request, req, res):
        # Ensure is attendee
        current_hackathon = Hackathon.objects.current()
        attendee_status = AttendeeStatus.objects.get_or_create(user=request.user, hackathon=current_hackathon)

        OrganizerInfo.objects.create(
            hackathon=current_hackathon,
            user=request.user,
            attendee_status=attendee_status,
            affiliation=req['affiliation'],
            teams=req['teams'],
            motivation=req['motivation']
        )

        acl.add_user_to_group(request.user, acl.group_pending_organizer)

        # Send email for confirmation
        email.send_template(
            to_email=request.user.email,
            to_first_name=request.user.first_name,
            to_last_name=request.user.last_name,
            subject='Organizer Registration Submitted!',
            template_name='organizer_register_waiting'
        )


