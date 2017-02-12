from api.models import UserInfo, Hackathon, AttendeeStatus, HackerInfo, MentorInfo, JudgeInfo, OrganizerInfo
from terminaltables import AsciiTable


USER_TYPES = ('hacker', 'mentor', 'judge', 'organizer')


def run():
    h = Hackathon.objects.current()

    # Create count dict for shirts[size][user_type]
    sizes = dict()
    for size in UserInfo.SHIRT_SIZE_CHOICES:
        sizes[size[0]] = dict()
        for user_type in USER_TYPES:
            sizes[size[0]][user_type] = 0

    # Count sizes
    attendee_statuses = AttendeeStatus.objects.filter(hackathon=h)
    for attendee in attendee_statuses:
        if hasattr(attendee.user, 'userinfo'):
            size = attendee.user.userinfo.shirt_size
        else:
            print('MISSING USER_ID FOR USER ' + attendee.user.email)
            continue

        if hasattr(attendee, 'hackerinfo'):
            sizes[size]['hacker'] += 1
        if hasattr(attendee, 'mentorinfo'):
            sizes[size]['mentor'] += 1
        if hasattr(attendee, 'judgeinfo'):
            sizes[size]['judge'] += 1
        if hasattr(attendee, 'organizerinfo'):
            sizes[size]['organizer'] += 1

    # Print in table
    title = 'Shirt sizes for REGISTERED attendees'
    headers = ['Shirt Size']
    headers.extend(USER_TYPES)
    data = []
    for size in UserInfo.SHIRT_SIZE_CHOICES:
        row = [size[1]]
        for user_type in USER_TYPES:
            row.append(sizes[size[0]][user_type])
        data.append(row)

    table_rows = [headers]
    table_rows.extend(data)
    table = AsciiTable(table_data=table_rows, title=title)
    print()
    print(table.table)
    print()
