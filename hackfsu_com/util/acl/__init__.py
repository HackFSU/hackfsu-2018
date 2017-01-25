from django.contrib.auth.models import User, Group
from .access_manager import AccessManager

group_user = 'user'     # Special case, just checks if logged in
group_admin = 'admin'   # Special case, just checks for admin flag

# Main user groups in db (just the ones we care about for the acl)
group_hacker = 'hacker'
group_mentor = 'mentor'
group_judge = 'judge'
group_organizer = 'organizer'

# Pending groups relevant for registration pages
group_pending_hacker = 'pending-hacker'
group_pending_mentor = 'pending-mentor'
group_pending_judge = 'pending-judge'
group_pending_organizer = 'pending-organizer'


groups = [
    group_user,
    group_hacker,
    group_mentor,
    group_judge,
    group_organizer,
    group_admin,
    group_pending_hacker,
    group_pending_mentor,
    group_pending_judge,
    group_pending_organizer
]


def add_user_to_group(user: User, group_name: str):
    group = Group.objects.get(name=group_name)
    if not user.groups.filter(name=group_name).exists():
        user.groups.add(group)
    user.save()


def remove_user_from_group(user: User, group_name: str):
    group = Group.objects.get(name=group_name)
    if user.groups.filter(name=group_name).exists():
        user.groups.remove(group)
    user.save()
