"""
    Initiates a password reset. Sends a password reset link to user's email.
"""
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl, captcha, email
from api.models import LinkKey
from datetime import timedelta
from django.utils import timezone


class RequestForm(forms.Form):
    g_recaptcha_response = forms.CharField(max_length=10000)
    email = forms.EmailField(max_length=100)


class StartResetView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_deny=[acl.group_user])

    def work(self, request, req: dict, res: dict):
        # Check captcha
        if not captcha.is_valid_response(req['g_recaptcha_response']):
            raise ValidationError('Captcha check failed', params=['g_recaptcha_response'])

        user = User.objects.filter(email=req['email'].lower())

        if user.exists():
            user = user[0]
        else:
            # Invalid, just ignore request
            return

        if LinkKey.objects.valid_key_exists_for_user(key_type=LinkKey.TYPE_PASSWORD_RESET, user=user):
            # Already has a pending reset
            return

        # Create key for password reset
        key = LinkKey.objects.create(
            user=user,
            type=LinkKey.TYPE_PASSWORD_RESET,
            key=LinkKey.generate_unique_key(),
            expires_at=(timezone.now() + timedelta(days=1))
        )

        # Send email with link to reset
        email.send_template_to_user(
            user=user, template_name='password_reset', subject='HackFSU Password Reset Link',
            merge_vars={'password_reset_link': key.get_link()}
        )
