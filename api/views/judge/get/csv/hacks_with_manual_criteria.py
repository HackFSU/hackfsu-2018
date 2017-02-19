"""
    Generates a CSV hacks and the manual criteria that should be looked at
"""

from hackfsu_com.views.generic import StreamedCsvView
from hackfsu_com.util import acl
from api.models import Hackathon, Hack, JudgingCriteria


class HacksWithManualCriteriaCsv(StreamedCsvView):
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
    file_name = 'HackFSU hacks with manual judging criteria.csv'

    @staticmethod
    def row_generator(request):
        h = Hackathon.objects.current()
        yield ['Table Number', 'Hack Name', 'Manual Judging Criteria']

        for hack in Hack.objects.filter(hackathon=h):
            row = [
                hack.table_number,
                hack.name,
            ]

            for criteria in hack.extra_judging_criteria.filter(status=JudgingCriteria.CRITERIA_TYPE_MANUAL)\
                    .order_by('id').all():
                row.append(criteria.name)

            yield row
