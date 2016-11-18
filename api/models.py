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

from django.db import models
from django.contrib.auth.models import User
# from django.contrib.postgres.fields import JSONField


class Test(models.Model):
    some_str = models.CharField(max_length=100)

# class AnonStat(models.Model):
#     """ TODO """
#     name = ""
#     option = ""
#
#
# class Hack(models.Model):
#     """ TODO """
#     categories = []
#     name = ""
#     table_number = 0
#     team = []
#
#
# class Hackathon(models.Model):
#     """ TODO """
#     current = False
#     start_date = ""
#     end_date = ""
#     mentors = 0
#     judges = 0
#     hackers_registered = 0
#     hackers_rsvp = 0
#     hackers_attended = 0
#     anon_stats = JSONField()
#     attendee_shirt_sizes = JSONField()
#
#
# class HackerInfo(models.Model):
#     """ TODO """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     is_first_hackathon = False
#     is_adult = True
#     agreed_to_mlh_data_sharing = False
#     school_name = ""
#     school_year = ""
#     school_major = ""
#     rsvp = False
#     checked_in = False
#
#
# class HelpRequest(models.Model):
#     """ TODO """
#     assigned_mentor = "user"
#     description = ""
#     location = ""
#     name = ""
#
#
# class JudgeInfo(models.Model):
#     """ TODO """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     affiliation = ""
#     comments = ""
#
#
# class MentorInfo(models.Model):
#     """ TODO """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     affiliation = ""
#     comments = ""
#
#
# class OldParseHacker(models.Model):
#     """ TODO """
#     parse_user = models.OneToOneField(OldParseUser, on_delete=models.CASCADE)
#     is_first_hackathon = False
#     is_adult = True
#     school_name = ""
#     school_year = ""
#     school_major = ""
#     misc_info = ""  # hate, jobs wanted, dev areas
#     final_status = ""
#
#
# class OldParseMentor(models.Model):
#     """ TODO """
#
#
# class OldParseUser(models.Model):
#     """ TODO """
#     email = ""
#     first_name = ""
#     last_name = ""
#     phone = ""
#     shirt_size = ""
#     diet = ""
#
#
# class Subscriber(models.Model):
#     """ TODO """
#     hackathon = "id"
#     email = ""
#
#
# class Sponsor(models.Model):
#     """ TODO """
#
#
# class Update(models.Model):
#     """ TODO """
#
#
# class UserInfo(models.Model):
#     """ TODO """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     last_hackathon = "hackathon link"
#     phone_number = ""
#     shirt_size = ""
#     diet = ""
#     waiver_signature = ""
#     github = ""
#
#
# class WifiCred(models.Model):
#     """ TODO """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)