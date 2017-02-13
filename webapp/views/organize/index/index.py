"""
    User Profile
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl


class IndexPage(PageView):
    template_name = 'organize/index/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
