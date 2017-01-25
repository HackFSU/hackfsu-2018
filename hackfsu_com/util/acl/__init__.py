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

db_groups = [
    group_hacker,
    group_mentor,
    group_judge,
    group_organizer,
    group_pending_hacker,
    group_pending_mentor,
    group_pending_judge,
    group_pending_organizer
]

groups = [
    group_user,
    group_admin,
]
groups.extend(db_groups)


def validate_db_group(group_name: str):
    if group_name not in db_groups:
        raise ValueError('Group "{}" is not a database group'.format(group_name))


def validate_db_groups(group_names: list):
    for name in group_names:
        validate_db_group(name)


def add_user_to_group(user: User, group_name: str):
    """ Adds user to a single group if not already in it """
    validate_db_group(group_name)
    group_to_add = Group.objects.get(name=group_name)
    if not user.groups.filter(name=group_to_add).exists():
        user.groups.add(group)
    user.save()


def remove_user_from_group(user: User, group_name: str):
    """ Removes user from a single group if in it """
    validate_db_group(group_name)
    matched_group = user.groups.filter(name=group_name)
    if matched_group.exists():
        user.groups.remove(matched_group)
    user.save()


def add_user_to_groups(user: User, group_names: list):
    """ Adds user to multiple groups if not already in them """
    validate_db_groups(group_names)
    groups_to_add = Group.objects.filter(name__in=[group_names])
    if groups_to_add.exists():
        for group in groups_to_add:
            if not user.group.filter(id=group.id).exists():
                user.groups.add(group)
    user.save()


def remove_user_from_groups(user: User, group_names: list):
    """ Removes user from multiple groups if in them """
    validate_db_groups(group_names)
    matched_groups = user.groups.filter(name__in=group_names)
    if matched_groups.exists():
        for group in matched_groups:
            user.groups.remove(group)
    user.save()
