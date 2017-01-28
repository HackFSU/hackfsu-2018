"""
    HackerInfos created before AttendeeStatuses were added do not have them. This corrects that.
"""

from api.models import HackerInfo, AttendeeStatus, Hackathon


def run():
    current_hackathon = Hackathon.objects.current()
    print('Getting hacker_info list...')
    hacker_info_without_attendee = HackerInfo.objects.filter(attendee_status=None)
    print(str(len(hacker_info_without_attendee)) + ' HackerInfo objects to modify')

    edits = 0
    for info in hacker_info_without_attendee:
        info.attendee_status = AttendeeStatus.objects.get_or_create(
            hackathon=current_hackathon,
            user=info.user
        )
        info.save()
        edits += 1
        print('created AttendeeStatus for ')

    print(str(edits) + ' HackerInfo objects modified')