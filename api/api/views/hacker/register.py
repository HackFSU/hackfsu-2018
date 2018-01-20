"""
    Hacker Registration
"""
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl, captcha, files, email
from api.models import UserInfo, HackerInfo, School, Hackathon, AttendeeStatus
import os


ACCEPTED_RESUME_CONTENT_TYPES = ['application/pdf']


class RequestForm(forms.Form):
    # User Register fields
    agree_to_mlh_coc = forms.BooleanField()                         # Must be true
    agree_to_mlh_data_sharing = forms.BooleanField()                # Must be true
    g_recaptcha_response = forms.CharField(max_length=10000, required=False)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(min_length=8, max_length=1000)
    shirt_size = forms.ChoiceField(choices=UserInfo.SHIRT_SIZE_CHOICES)
    phone_number = forms.CharField(max_length=20)
    github = forms.CharField(required=False, max_length=100)
    linkedin = forms.CharField(required=False, max_length=200)
    diet = forms.CharField(required=False, max_length=500)

    # OG Hacker Fields
    is_first_hackathon = forms.BooleanField(required=False)
    is_adult = forms.BooleanField(required=False)
    is_high_school = forms.BooleanField(required=False)   # make this a select box for College/HS Student
    school_year = forms.ChoiceField(choices=HackerInfo.SCHOOL_YEAR_CHOICES)
    school_major = forms.CharField(max_length=100)
    interests = forms.CharField(required=False, max_length=500)
    new_school_name = forms.CharField(required=False, max_length=100)
    school_id = forms.IntegerField(required=False)
    resume = forms.FileField(required=False)


class RegisterView(ApiView):
    request_form_class = RequestForm
    allowed_after_current_hackathon_ends = True
    # access_manager = acl.AccessManager(acl_accept=[acl.group_user],
    #                                    acl_deny=[acl.group_hacker, acl.group_judge, acl.group_organizer,
    #                                              acl.group_pending_hacker, acl.group_pending_judge,
    #                                              acl.group_pending_organizer])

    def work(self, request, req, res):

        #
        #   User Registration
        #

        # Clean fields
        req['email'] = req['email'].lower()
        req['first_name'] = req['first_name'].lower().capitalize()

        # Check captcha
        if not captcha.is_valid_response(req['g_recaptcha_response']):
            raise ValidationError('Captcha check failed', params=['g_recaptcha_response'])

        # Check if email (username) already in use
        if User.objects.filter(username=req['email']).exists():
            raise ValidationError('Email already in use', params=['email'])

        # Validate the resume upload (from OG hacker reg)
        resume_file_name = ''
        if request.FILES and request.FILES['resume']:
            resume_file = request.FILES['resume']
            file_name, file_extension = os.path.splitext(resume_file.name.lower())

            if resume_file.content_type not in ACCEPTED_RESUME_CONTENT_TYPES:
                raise ValidationError('Invalid resume file type "{}". Valid options include {}'.format(
                    resume_file.content_type,
                    ', '.join(ACCEPTED_RESUME_CONTENT_TYPES)
                ), params=['resume'])

        # Attempt to create new user
        user = User.objects.create_user(
            username=req['email'],
            email=req['email'],
            password=req['password']
        )
        user.first_name = req['first_name']
        user.last_name = req['last_name']
        user.save()

        # Create respective UserInfo
        user_info = UserInfo(
            user=user,
            shirt_size=req['shirt_size'],
            github=req['github'],
            linkedin=req['linkedin'],
            diet=req['diet'],
            phone_number=req['phone_number']
        )
        user_info.save()


        #
        #   OG Hacker Registration
        #

        # Actually load resume Load resume
        resume_file_name = ''
        if request.FILES and request.FILES['resume']:
            resume_file = request.FILES['resume']
            file_name, file_extension = os.path.splitext(resume_file.name.lower())

            resume_file_name = files.handle_file_upload(
                src_file_name="resume_{}_{}_{}".format(
                    user.id,
                    user.first_name.lower(),
                    user.last_name.lower()
                ),
                file=request.FILES['resume'],
                file_extension=file_extension,
                media_directory_path=('resumes/' + str(Hackathon.objects.current().id) + '/')
            )

        # Get school object (creating one if needed)
        school = self.get_school(school_id=req['school_id'], new_school_name=req['new_school_name'],
                                 hs=req['is_high_school'])

        # Ensure is attendee
        current_hackathon = Hackathon.objects.current()
        attendee_status = AttendeeStatus.objects.get_or_create(user=user, hackathon=current_hackathon)

        # Create Info object
        HackerInfo.objects.create(
            user=user,
            hackathon=current_hackathon,
            attendee_status=attendee_status,
            school=school,
            is_first_hackathon=req['is_first_hackathon'],
            is_adult=req['is_adult'],
            school_major=req['school_major'],
            school_year=req['school_year'],
            resume_file_name=resume_file_name,
            interests=req['interests']
        )

        # Add to pending group
        acl.add_user_to_group(user, acl.group_pending_hacker)

        # Send email for confirmation
        email.send_template(
            to_email=user.email,
            to_first_name=user.first_name,
            to_last_name=user.last_name,
            subject='Hacker Registration Submitted!',
            template_name='hacker_register_waiting'
        )

    @staticmethod
    def get_school(school_id, new_school_name, hs):
        """ Gets school or saves a new school if needed """

        if school_id is not None:
            try:
                return School.objects.get(id=school_id)
            except ObjectDoesNotExist:
                raise ValidationError('Invalid school', params=['school_id'])

        if new_school_name is None or len(new_school_name.strip()) == 0:
            raise ValidationError('Invalid school', params=['new_school_name'])

        school = School.objects.filter(name=new_school_name.strip())
        if school.exists():
            return school[0]
        else:
            # Valid new school, add it to database
            return School.objects.create(
                name=new_school_name.strip(),
                user_submitted=True,
                type=('H' if hs is True else 'C')
            )
