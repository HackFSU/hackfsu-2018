"""
    Generates a CSV containing approved hackers' resumes
"""

from hackfsu_com.views.generic import StreamedCsvView
from hackfsu_com.util import acl, files
from django.conf import settings
from api.models import Hackathon, HackerInfo, UserInfo


class ResumeLinksCsv(StreamedCsvView):
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
    file_name = 'HackFSU Approved Hackers\' Submitted Resumes.csv'

    @staticmethod
    def row_generator(request):
        h = Hackathon.objects.current()
        yield ['Approved Hackers\' Submitted Resumes']
        yield [
            'First Name',
            'Last Name',
            'Email',
            'School',
            'Github',
            'LinkedIn',
            'Attended',
            'Resume File Name',
            'Resume URL'
        ]

        for hacker in HackerInfo.objects.filter(
            hackathon=h,
            approved=True
        ):
            user_info = UserInfo.objects.get(user=hacker.user)
            row = [
                hacker.user.first_name,
                hacker.user.last_name,
                hacker.user.email,
                str(hacker.school),
                user_info.github,
                user_info.linkedin,
                hacker.attendee_status.checked_in_at is not None
            ]

            if len(hacker.resume_file_name) > 0:
                row.extend([
                    hacker.resume_file_name.split('/')[-1],
                    settings.URL_BASE + files.get_url(hacker.resume_file_name)
                ])

            yield row
