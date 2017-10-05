"""
    User Profile
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl


class ProfilePage(PageView):
    template_name = 'user/profile/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_user])
