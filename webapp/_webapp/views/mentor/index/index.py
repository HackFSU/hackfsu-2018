"""
    View all help requests
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl


class IndexPage(PageView):
    template_name = 'mentor/index/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_mentor])
