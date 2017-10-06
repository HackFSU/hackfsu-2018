"""
    Organizer user registration
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl


class OrganizerRegistrationPage(PageView):
    template_name = 'registration/organizer/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_user],
                                       acl_deny=[acl.group_hacker, acl.group_organizer,
                                                 acl.group_pending_hacker, acl.group_pending_organizer])
