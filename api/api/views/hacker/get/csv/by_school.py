"""
    Generates a CSV containing hacker data with school name
"""

from hackfsu_com.views.generic import StreamedCsvView
from hackfsu_com.util import acl
from api.models import Hackathon, HackerInfo


class BySchoolCsv(StreamedCsvView):
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
    file_name = 'hackers_by_school.csv'

    @staticmethod
    def row_generator(request):
        h = Hackathon.objects.current()
        yield ['School', 'First Name', 'Last Name', 'Email', 'RSVP=yes']

        for hacker in HackerInfo.objects.filter(hackathon=h, approved=True):
            yield [
                str(hacker.school),
                hacker.user.first_name,
                hacker.user.last_name,
                hacker.user.email,
                'Y' if hacker.attendee_status.rsvp_result else ''
            ]
