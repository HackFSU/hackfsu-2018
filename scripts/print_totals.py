from django.contrib.auth.models import User
from api.models import Hackathon, AttendeeStatus
from terminaltables import AsciiTable
from datetime import datetime
from dateutil import tz


def print_hackathon_attendees(hackathon: Hackathon):
    title = str(hackathon)
    data = (
        ('Group', 'Registered', 'Approved', 'RSVP\'d', 'Checked-in'),
        (
            'All',
            AttendeeStatus.objects.filter(hackathon=hackathon).count(),
            'n/a',
            AttendeeStatus.objects.filter(hackathon=hackathon, rsvp_confirmed=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, checked_in=True).count(),
        ),
        (
            'Hackers',
            AttendeeStatus.objects.filter(hackathon=hackathon, hackerinfo__isnull=False).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, hackerinfo__isnull=False,
                                          hackerinfo__approved=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, hackerinfo__isnull=False, rsvp_confirmed=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, hackerinfo__isnull=False, checked_in=True).count(),
        ),
        (
            'Mentors',
            AttendeeStatus.objects.filter(hackathon=hackathon, mentorinfo__isnull=False).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, mentorinfo__isnull=False,
                                          mentorinfo__approved=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, mentorinfo__isnull=False, rsvp_confirmed=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, mentorinfo__isnull=False, checked_in=True).count(),
        ),
        (
            'Judges',
            AttendeeStatus.objects.filter(hackathon=hackathon, judgeinfo__isnull=False).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, judgeinfo__isnull=False,
                                          judgeinfo__approved=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, judgeinfo__isnull=False, rsvp_confirmed=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, judgeinfo__isnull=False, checked_in=True).count(),
        ),
        (
            'Organizers',
            AttendeeStatus.objects.filter(hackathon=hackathon, organizerinfo__isnull=False).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, organizerinfo__isnull=False,
                                          organizerinfo__approved=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, organizerinfo__isnull=False, rsvp_confirmed=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, organizerinfo__isnull=False, checked_in=True).count(),
        ),
    )

    table = AsciiTable(table_data=data, title=title)
    print(table.table)
    print()


def print_error_checks():
    title = 'Error Checks'
    data = (
        ('Check', 'Errors found'),
        ('Users without UserInfo objects', User.objects.filter(userinfo=None).count())
    )
    table = AsciiTable(table_data=data, title=title)
    print(table.table)
    print()


def print_accounts():
    title = 'Accounts'
    data = (
        ('', 'Count'),
        ('Users', User.objects.count()),
        ('Unassigned', User.objects.filter(attendeestatus=None).count())
    )
    table = AsciiTable(table_data=data, title=title)
    print(table.table)
    print()


def print_now():
    now = datetime.now(tz.gettz('EST'))
    print('{} ({})'.format(now.strftime('Totals as of %c'), now.tzname()))


def run():
    print_now()
    print_error_checks()
    print_accounts()
    print_hackathon_attendees(Hackathon.objects.current())

