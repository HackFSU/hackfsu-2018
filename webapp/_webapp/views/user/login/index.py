"""
    User log in
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl


class LoginPage(PageView):
    template_name = 'user/login/index.html'
    access_manager = acl.AccessManager(acl_deny=[acl.group_user])

    def get_access_denied_redirect_url(self, request):
        # Don't bother with the access denied flag, just redirect them to profile
        return '/user/profile'
