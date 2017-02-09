"""
    User Profile
"""

from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl
from api.models import AttendeeStatus, Hackathon


class RsvpPage(PageView):
    template_name = 'user/rsvp/index.html'
    access_manager = acl.AccessManager(acl_accept=[
        acl.group_hacker,
        acl.group_mentor,
        acl.group_organizer,
        acl.group_judge
    ])

    def authenticate(self, request):
        # Keep group check
        if not super().authenticate(request):
            return False

        # Add check to make sure not already RSVP'd
        return AttendeeStatus.objects.filter(
            hackathon=Hackathon.objects.current(), user=request.user, rsvp_submitted_at__isnull=True
        ).exists()
