from .access_manager import AccessManager

group_user = 'user'     # Special case, just checks if logged in

# Groups in user db (just the ones we care about for the acl)
group_hacker = 'hacker'
group_mentor = 'mentor'
group_judge = 'judge'
group_organizer = 'organizer'
group_admin = 'admin'

groups = [
    group_user,
    group_hacker,
    group_mentor,
    group_judge,
    group_organizer,
    group_admin
]

