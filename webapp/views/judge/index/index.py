"""
    Public hack roster
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl


class IndexPage(PageView):
    template_name = 'judge/index/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_judge])
