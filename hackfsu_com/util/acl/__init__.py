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

