"""
    Public hack roster
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl


class ExpoPage(PageView):
    template_name = 'organize/judging/expo/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
