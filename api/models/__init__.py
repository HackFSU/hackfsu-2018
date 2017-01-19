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
from .anon_stat import AnonStat
from .user_info import UserInfo
from .hacker_info import HackerInfo
from .judge_info import JudgeInfo
from .mentor_info import MentorInfo
from .organizer_info import OrganizerInfo
from .help_request import HelpRequest
from .school import School
from .subscriber import Subscriber
from .wifi_cred import WifiCred
# TODO Update
# TODO Sponsor
# TODO OldParseUser
# TODO OldParseHacker
# TODO OldParseMentor
