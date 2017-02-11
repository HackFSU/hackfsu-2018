from django.contrib.auth.models import User
from api.models import Hackathon, AttendeeStatus, MentorInfo, HackerInfo, HelpRequest, JudgeInfo, OrganizerInfo
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
            AttendeeStatus.objects.filter(hackathon=hackathon, rsvp_result=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, checked_in_at__isnull=False).count(),
        ),
        (
            'Hackers',
            AttendeeStatus.objects.filter(hackathon=hackathon, hackerinfo__isnull=False).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, hackerinfo__isnull=False,
                                          hackerinfo__approved=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, hackerinfo__isnull=False, rsvp_result=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, hackerinfo__isnull=False, checked_in_at__isnull=False).count(),
        ),
        (
            'Mentors',
            AttendeeStatus.objects.filter(hackathon=hackathon, mentorinfo__isnull=False).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, mentorinfo__isnull=False,
                                          mentorinfo__approved=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, mentorinfo__isnull=False, rsvp_result=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, mentorinfo__isnull=False,
                                          checked_in_at__isnull=False).count(),
        ),
        (
            'Judges',
            AttendeeStatus.objects.filter(hackathon=hackathon, judgeinfo__isnull=False).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, judgeinfo__isnull=False,
                                          judgeinfo__approved=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, judgeinfo__isnull=False, rsvp_result=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, judgeinfo__isnull=False,
                                          checked_in_at__isnull=False).count(),
        ),
        (
            'Organizers',
            AttendeeStatus.objects.filter(hackathon=hackathon, organizerinfo__isnull=False).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, organizerinfo__isnull=False,
                                          organizerinfo__approved=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, organizerinfo__isnull=False, rsvp_result=True).count(),
            AttendeeStatus.objects.filter(hackathon=hackathon, organizerinfo__isnull=False,
                                          checked_in_at__isnull=False).count(),
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


def print_school_totals(h: Hackathon):
    title = 'Hacker totals by school'

    school_counts = {}

    for hacker in HackerInfo.objects.filter(hackathon=h):
        if hacker.school not in school_counts:
            school_counts[hacker.school] = {
                'registered': 0,
                'approved': 0,
                'rsvp': 0,
                'checked-in': 0
            }
        school_counts[hacker.school]['registered'] += 1

        if hacker.approved:
            school_counts[hacker.school]['approved'] += 1

        if hacker.attendee_status.rsvp_result:
            school_counts[hacker.school]['rsvp'] += 1

        if hacker.attendee_status.checked_in_at is not None:
            school_counts[hacker.school]['checked-in'] += 1

    table_rows = [('School', 'Registered', 'Approved', 'RSVP\'d', 'Checked-in')]

    totals = {
        'registered': 0,
        'approved': 0,
        'rsvp': 0,
        'checked-in': 0
    }

    data = []
    for school, counts in school_counts.items():
        data.append((
            school.name + (' [U]' if school.user_submitted else ''),
            counts['registered'],
            counts['approved'],
            counts['rsvp'],
            counts['checked-in']
        ))
        for key in counts:
            totals[key] += counts[key]

    # Sort by school name
    data.sort(key=lambda x: x[0])

    data.append((
        '*** TOTALS ***',
        str(totals['registered']),
        str(totals['approved']),
        str(totals['rsvp']),
        str(totals['checked-in']),
    ))

    table_rows.extend(data)

    table = AsciiTable(table_data=table_rows, title=title)
    print(table.table)
    print()


def print_mentors(h: Hackathon):
    title = 'Mentors'

    table_rows = [('Name', 'Approved?', 'RSVP\'d?', 'Checked-in?', 'Help Requests Claimed')]
    data = []

    mentors = MentorInfo.objects.filter(hackathon=h)
    for mentor in mentors:
        data.append((
            '{} {}'.format(mentor.user.first_name, mentor.user.last_name),
            'Yes' if mentor.approved else '',
            'Yes' if mentor.attendee_status.rsvp_result else '',
            'Yes' if mentor.attendee_status.checked_in_at is not None else '',
            HelpRequest.objects.filter(assigned_mentor=mentor).count()
        ))

    data.sort(key=lambda x: x[0])
    table_rows.extend(data)
    table = AsciiTable(table_data=table_rows, title=title)
    print(table.table)
    print()


def print_judges(h: Hackathon):
    title = 'Judges'

    table_rows = [('Name', 'Approved?', 'RSVP\'d?', 'Checked-in?')]
    data = []

    judges = JudgeInfo.objects.filter(hackathon=h)
    for judge in judges:
        data.append((
            '{} {}'.format(judge.user.first_name, judge.user.last_name),
            'Yes' if judge.approved else '',
            'Yes' if judge.attendee_status.rsvp_result else '',
            'Yes' if judge.attendee_status.checked_in_at is not None else ''
        ))

    data.sort(key=lambda x: x[0])
    table_rows.extend(data)
    table = AsciiTable(table_data=table_rows, title=title)
    print(table.table)
    print()


def print_organizers(h: Hackathon):
    title = 'Organizers'

    table_rows = [('Name', 'Approved?', 'RSVP\'d?', 'Checked-in?')]
    data = []

    organizers = OrganizerInfo.objects.filter(hackathon=h)
    for organizer in organizers:
        data.append((
            '{} {}'.format(organizer.user.first_name, organizer.user.last_name),
            'Yes' if organizer.approved else '',
            'Yes' if organizer.attendee_status.rsvp_result else '',
            'Yes' if organizer.attendee_status.checked_in_at is not None else ''
        ))

    data.sort(key=lambda x: x[0])
    table_rows.extend(data)
    table = AsciiTable(table_data=table_rows, title=title)
    print(table.table)
    print()


def run():
    current_hackathon = Hackathon.objects.current()
    print_now()
    print_error_checks()
    print_accounts()
    print_hackathon_attendees(current_hackathon)
    print_school_totals(current_hackathon)
    print_mentors(current_hackathon)
    print_judges(current_hackathon)
    print_organizers(current_hackathon)
