"""
    Hacker Registration
"""
from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import logout
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl, files, email
from api.models import HackerInfo, School, Hackathon


class RequestForm(forms.Form):
    is_first_hackathon = forms.BooleanField()
    is_adult = forms.BooleanField()
    is_high_school = forms.BooleanField()   # make this a select box for College/HS Student
    school_year = forms.ChoiceField(choices=HackerInfo.SCHOOL_YEAR_CHOICES)
    school_major = forms.CharField(max_length=100)
    interests = forms.CharField(required=False, max_length=500)
    new_school_name = forms.CharField(required=False, max_length=100)
    school_id = forms.IntegerField(required=False)
    resume = forms.FileField(required=False)

    # TODO more fields


class RegisterView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_user],
                                       acl_deny=[acl.group_hacker, acl.group_judge, acl.group_organizer,
                                                 acl.group_pending_hacker, acl.group_pending_judge,
                                                 acl.group_pending_organizer])

    def work(self, request, req, res):
        # Load resume
        resume_file_name = None
        if request.FILES and request.FILES['resume']:
            resume_file_name = files.handle_file_upload(
                file=request.FILES['resume']
            )

        # Get school object (creating one if needed)
        school = self.get_school(school_id=req['school_id'], new_school_name=req['new_school_name'],
                                 hs=res['is_high_school'])
        # Create Info object
        HackerInfo.objects.create(
            user=request.user,
            hackathon=Hackathon.objects.current(),
            school=school,
            is_first_hackathon=req['is_first_hackathon'],
            is_adult=req['is_adult'],
            school_major=['school_major'],
            resume_file_name=resume_file_name,
            interests=req['interests'],
            comments='swamphacks',  # TODO remove
        )

        # Add to pending group
        acl.add_user_to_group(request.user, acl.group_pending_hacker)

        # Send email for confirmation
        email.send_template(
            to_email=request.user.email,
            to_first_name=request.user.first_name,
            to_last_name=request.user.last_name,
            subject='Hacker Registration Submitted!',
            template_name='hacker_registered'
        )

        # TODO remove, only for temp
        logout(request)

    @staticmethod
    def get_school(school_id, new_school_name, hs):
        """ Gets school or saves a new school if needed """

        if school_id is not None:
            try:
                return School.objects.get(id=school_id)
            except ObjectDoesNotExist:
                raise ValidationError('Invalid school', params=['school_id'])

        if new_school_name is None or len(new_school_name.trim()) == 0:
            raise ValidationError('Invalid school', params=['new_school_name'])

        school = School.objects.filter(name=new_school_name.trim())
        if school.exists():
            return school
        else:
            # Valid new school, add it to database
            return School.objects.create(
                name=new_school_name.trim(),
                user_submitted=True,
                type=('H' if hs is True else 'C')
            )
