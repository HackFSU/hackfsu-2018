"""
    Access Manager class
"""

from hackfsu_com.util import acl
from django.contrib.auth.models import User
from copy import copy


def is_valid_acl(group_list):
    """ Makes sure the group_list contains only valid group entries from acl.groups """
    for group in group_list:
        if group not in acl.groups:
            return False
    return True


class AccessManager(object):
    """
        Access Control List (ACL) container for accept and deny lists.
         - Uses ACL groups defined in acl.groups
         - Checks list entries for validity at initialization.
         - Can be used to check users.
         - To pass the check, one must belong to one of the accepted groups (if any exist) and none of the denied.
    """
    def __init__(self, acl_accept=None, acl_deny=None):
        # Empty ACLs by default
        if acl_accept is None:
            acl_accept = []
        if acl_deny is None:
            acl_deny = []

        if is_valid_acl(acl_accept):
            self.acl_accept = copy(acl_accept)
        else:
            raise ValueError('Invalid ACL for accepted groups')

        if is_valid_acl(acl_deny):
            self.acl_deny = copy(acl_deny)
        else:
            raise ValueError('Invalid ACL for denied groups')

        # Check for groups both allowed and denied
        for group in self.acl_accept:
            if group in self.acl_deny:
                raise ValueError('Cannot both accept and deny group ' + group)

        # Handle special 'user' group for logged in users
        self.allow_anon_users = True
        self.require_anon_users = False

        if acl.group_user in self.acl_accept:
            self.acl_accept.remove(acl.group_user)
            self.allow_anon_users = False
        elif acl.group_user in self.acl_deny:
            self.acl_deny.remove(acl.group_user)
            self.require_anon_users = True

    def check_user(self, user: User):
        """ Validates a Django user against the ACL """

        if user is None:
            return False

        # Check 'user' group flags
        if user.is_authenticated:
            # Valid User is logged in
            if self.require_anon_users:
                return False
        else:
            # Anonymous user, not logged in
            return self.allow_anon_users

        if (len(self.acl_accept) + len(self.acl_deny)) == 0:
            # No additional ACL to enforce
            return True

        # Load groups user is a part of from db
        user_groups = user.groups.all()

        # Preform accept/deny checks
        for group in self.acl_accept:
            if group not in user_groups:
                return False
        for group in self.acl_deny:
            if group in user_groups:
                return False

        # All checks passed
        return True
