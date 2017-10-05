"""
    Completes the password reset
"""

from hackfsu_com.views.generic import PageView
from api.models import LinkKey
from api.views.user.password.complete_reset import SESSION_KEY


class CompleteResetPage(PageView):
    template_name = 'user/password/complete_reset/index.html'

    def authenticate(self, request):
        # Keep group check
        if not super().authenticate(request):
            return False

        # Make sure key is correct and store it in session
        key = self.kwargs['link_key']

        if LinkKey.objects.valid_key_exists(key_type=LinkKey.TYPE_PASSWORD_RESET, key=key):
            request.session[SESSION_KEY] = key
            return True

        # Bad key
        return False


