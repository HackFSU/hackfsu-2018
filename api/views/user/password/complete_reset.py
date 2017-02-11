"""
    Completes password reset. Must have password reset key in session from going to reset page
"""

from django import forms
from django.contrib.auth import logout
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import email
from api.models import LinkKey
from django.utils import timezone
SESSION_KEY = 'reset_password'


class RequestForm(forms.Form):
    new_password = forms.CharField(min_length=8, max_length=1000)


class CompleteResetView(ApiView):
    request_form_class = RequestForm

    def work(self, request, req: dict, res: dict):
        link_key = LinkKey.objects.get(key=request.session.get(SESSION_KEY))
        user = link_key.user
        user.set_password(req['new_password'])
        user.save()

        email.send_template_to_user(user=user, template_name='password_changed',
                                    subject='HackFSU Password Change Successful')

        logout(request)

        link_key.used_at = timezone.now()
        link_key.save()

    def authenticate(self, request):
        return super().authenticate(request)\
               and LinkKey.objects.valid_key_exists(key_type=LinkKey.TYPE_PASSWORD_RESET,
                                                    key=request.session.get(SESSION_KEY))


