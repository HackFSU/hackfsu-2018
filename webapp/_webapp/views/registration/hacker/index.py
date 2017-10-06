"""
    Hacker user registration
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl


class HackerRegistrationPage(PageView):
    allowed_after_current_hackathon_ends = False
    template_name = 'registration/hacker/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_user],
                                       acl_deny=[acl.group_hacker, acl.group_judge, acl.group_organizer,
                                                 acl.group_pending_hacker, acl.group_pending_judge,
                                                 acl.group_pending_organizer])
