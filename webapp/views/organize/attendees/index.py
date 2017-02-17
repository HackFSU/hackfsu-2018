"""
    Organize attendees
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl


class AttendeesPage(PageView):
    template_name = 'organize/attendees/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
