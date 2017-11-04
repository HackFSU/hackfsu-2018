"""
    Mentor registration
"""
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl, email
from api.models import MentorInfo, Hackathon, AttendeeStatus


class RequestForm(forms.Form):
    affiliation = forms.CharField(max_length=100)
    skills = forms.CharField(max_length=1000)
    motivation = forms.CharField(max_length=1000)
    availability = forms.IntegerField(min_value=0, max_value=MentorInfo.MAX_AVAILABILITY)


class RegisterView(ApiView):
    allowed_after_current_hackathon_ends = False
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_user],
                                       acl_deny=[acl.group_mentor, acl.group_pending_mentor])

    def work(self, request, req, res):
        # Ensure is attendee
        current_hackathon = Hackathon.objects.current()
        attendee_status = AttendeeStatus.objects.get_or_create(user=request.user, hackathon=current_hackathon)

        MentorInfo.objects.create(
            hackathon=current_hackathon,
            user=request.user,
            attendee_status=attendee_status,
            affiliation=req['affiliation'],
            skills=req['skills'],
            motivation=req['motivation'],
            availability=req['availability']
        )

        acl.add_user_to_group(request.user, acl.group_pending_mentor)

        # Send email for confirmation
        email.send_template(
            to_email=request.user.email,
            to_first_name=request.user.first_name,
            to_last_name=request.user.last_name,
            subject='Mentor Registration Submitted!',
            template_name='mentor_register_waiting'
        )


