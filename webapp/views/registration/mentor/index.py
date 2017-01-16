"""
    Mentor user registration
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl


class MentorRegistrationPage(PageView):
    template_name = 'registration/mentor/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_user], acl_deny=[acl.group_mentor])
