"""
    Generates a CSV of all checked in users
"""

from hackfsu_com.views.generic import StreamedCsvView
from hackfsu_com.util import acl
from api.models import Hackathon, AttendeeStatus


class AttendeesCheckedInCsv(StreamedCsvView):
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
    file_name = 'Checked in Attendees.csv'

    @staticmethod
    def row_generator(request):
        h = Hackathon.objects.current()
        yield ['First Name', 'Last Name', 'Groups']

        for status in AttendeeStatus.objects.filter(hackathon=h, checked_in_at__isnull=False):
            yield [
                status.user.first_name,
                status.user.last_name,
                ' '.join(status.user.groups.values_list('name', flat=True))
            ]
