"""
    User account registration. Creates basic user account
"""
from django import forms
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl, captcha, email
from api.models import UserInfo
from api.views.user.login import log_user_in


class RequestForm(forms.Form):
    agree_to_mlh_coc = forms.BooleanField()                         # Must be true
    agree_to_mlh_data_sharing = forms.BooleanField()                # Must be true
    g_recaptcha_response = forms.CharField(max_length=10000)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=1000)
    shirt_size = forms.ChoiceField(choices=UserInfo.SHIRT_SIZE_CHOICES)
    phone_number = forms.CharField(max_length=20)
    github = forms.CharField(required=False, max_length=100)
    linkedin = forms.CharField(required=False, max_length=200)
    diet = forms.CharField(required=False, max_length=500)


class ResponseForm(forms.Form):
    logged_in = forms.BooleanField(required=False)


class RegisterView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_deny=[acl.group_user])

    def work(self, request: HttpRequest, req: dict, res: dict):
        # Clean fields
        req['email'] = req['email'].lower()
        req['first_name'] = req['first_name'].lower().capitalize()

        # Check captcha
        if not captcha.is_valid_response(req['g_recaptcha_response']):
            raise ValidationError('Captcha check failed', params=['g_recaptcha_response'])

        # Check if email (username) already in use
        if User.objects.filter(username=req['email']).exists():
            raise ValidationError('Email already in use', params=['email'])

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

        # Send email for confirmation
        email.send_template(
            to_email=req['email'],
            to_first_name=req['first_name'],
            to_last_name=req['last_name'],
            subject='HackFSU Account Created',
            template_name='user_registered'
        )

        # Log user in
        try:
            log_user_in(request=request, email=req['email'], password=req['password'])
            res['logged_in'] = True
        except ValidationError:
            res['logged_in'] = False
