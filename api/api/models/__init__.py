"""

The Django User class is used to handle users and authentication.
https://docs.djangoproject.com/en/1.10/ref/contrib/auth/

User groups:
    superadmin - Can access django admin page
    admin - Can access regular admin pages
    hacker - Hacker pages
    mentor - Mentor pages
    judge - Judge pages
    user (implied when logged in) - User pages

"""

from .hackathon import Hackathon
from .hackathon_countdown import HackathonCountdown
from .hackathon_map import HackathonMap
from .hackathon_sponsor import HackathonSponsor
from .hackathon_update import HackathonUpdate
from .attendee_status import AttendeeStatus
from .schedule_item import ScheduleItem
from .school import School
from .anon_stat import AnonStat
from .user_info import UserInfo
from .hacker_info import HackerInfo
from .judge_info import JudgeInfo
from .mentor_info import MentorInfo
from .organizer_info import OrganizerInfo
from .help_request import HelpRequest
from .subscriber import Subscriber
from .wifi_cred import WifiCred
from .link_key import LinkKey
from .hackathon_prize import HackathonPrize
from .judging_expo import JudgingExpo
from .judging_criteria import JudgingCriteria
from .hack import Hack
from .judging_grade import JudgingGrade
from .judging_assignment import JudgingAssignment
from .preview_email import PreviewEmail
from .nomination import Nomination
from .scan_event import ScanEvent
from .scan_record import ScanRecord

# TODO OldParseUser
# TODO OldParseHacker
# TODO OldParseMentor
