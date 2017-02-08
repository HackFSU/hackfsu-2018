"""
    Prints the schedule in the local time zone
"""

from api.models import ScheduleItem, Hackathon
from datetime import datetime
from terminaltables import AsciiTable
import pytz


EASTERN = pytz.timezone('US/Eastern')


def format_time(dt: datetime):
    dt = dt.astimezone(tz=EASTERN)
    return dt.strftime('%a %I:%M %p')


def run():
    h = Hackathon.objects.current()
    items = ScheduleItem.objects.filter(hackathon=h).order_by('start', 'end')

    title = '{} Schedule in {}'.format(h.name, EASTERN.zone)
    data = [('Start', 'End', 'Event Name')]

    for item in items:
        data.append((
            format_time(item.start),
            format_time(item.end) if item.end is not None else 'n/a',
            item.name
        ))

    table = AsciiTable(table_data=data, title=title)
    print(table.table)
