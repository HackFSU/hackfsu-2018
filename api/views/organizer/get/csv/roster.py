"""
    Generates a CSV containing hacker data with school name
"""

from hackfsu_com.views.generic import StreamedCsvView
from hackfsu_com.util import acl
from api.models import Hackathon, OrganizerInfo


class RosterCsv(StreamedCsvView):
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
    file_name = 'organizer_roster.csv'

    @staticmethod
    def row_generator(request):
        h = Hackathon.objects.current()
        yield ['First Name', 'Last Name']

        for info in OrganizerInfo.objects.filter(hackathon=h, approved=True):
            yield [
                info.user.first_name,
                info.user.last_name
            ]
