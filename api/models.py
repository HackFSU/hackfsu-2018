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
from django.contrib.postgres.fields import JSONField


class Hackathon(models.Model):
    current = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    statistics = JSONField(default=None, null=True, blank=True)    # Snapshot of info grabbed from db
    # mentors = 0
    # judges = 0
    # hackers_registered = 0
    # hackers_rsvp = 0
    # hackers_attended = 0
    # anon_stats = JSONField()
    # attendee_shirt_sizes = JSONField()


class AnonStat(models.Model):
    KEY_CHOICES = (
        ('GEN', 'Gender'),
        ('ETH', 'Ethnicity')
    )

    VALUE_CHOICES = (
        ('Gender', (
            ('MAL', 'Male'),
            ('FEM', 'Female'),
            ('OTH', 'Other')
        )),
        ('Ethnicity', (
            ('ASI', 'Asian'),
            ('BLK', 'Black'),
            ('HIS', 'Hispanic'),
            ('MLT', 'Multicultural'),
            ('WHT', 'White'),
            ('OTH', 'Other')
        ))
    )

    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    key = models.CharField(max_length=3, choices=KEY_CHOICES)
    value = models.CharField(max_length=3, choices=VALUE_CHOICES)


class UserInfo(models.Model):
    SHIRT_SIZE_CHOICES = (
        ('m-s',     'Men\'s Small'),
        ('m-m',     'Men\'s Medium'),
        ('m-l',     'Men\'s Large'),
        ('m-xl',    'Men\'s XL'),
        ('m-2xl',   'Men\'s XXL'),
        ('m-3xl',   'Men\'s XXXL'),
        ('w-s',     'Women\'s Small'),
        ('w-m',     'Women\'s Medium'),
        ('w-l',     'Women\'s Large'),
        ('w-xl',    'Women\'s XL')
    )

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    shirt_size = models.CharField(max_length=3, choices=SHIRT_SIZE_CHOICES)
    waiver_signature = models.CharField(max_length=100)
    diet = models.CharField(max_length=500, default='', blank=True)
    github = models.CharField(max_length=100, default='', blank=True)
    last_hackathon = models.ForeignKey(to=Hackathon, on_delete=models.SET_NULL, default=None, null=True, blank=True)


class HackerInfo(models.Model):
    SCHOOL_YEAR_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    is_first_hackathon = models.BooleanField()
    is_adult = models.BooleanField()
    agreed_to_mlh_data_sharing = models.BooleanField()
    school_name = models.CharField(max_length=100)
    school_year = models.CharField(max_length=2, choices=SCHOOL_YEAR_CHOICES)
    school_major = models.CharField(max_length=100)
    rsvp = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)


class JudgeInfo(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=100)
    comments = models.CharField(max_length=1000, default='', blank=True)


class MentorInfo(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=100)
    comments = models.CharField(max_length=1000, default='', blank=True)


class HelpRequest(models.Model):
    description = models.CharField(max_length=1000)
    location = models.CharField(max_length=100)
    attendee_name = models.CharField(max_length=100)
    assigned_mentor = models.ForeignKey(to=MentorInfo, on_delete=models.SET_NULL, default=None, null=True, blank=True)


class School(models.Model):
    TYPE_CHOICES = (
        ('H', 'High School'),
        ('C', 'College')
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='C')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, default='', blank=True)


class Subscriber(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()


class WifiCred(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    assigned_user = models.OneToOneField(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)


# class Hack(models.Model):
#     categories = []
#     name = ""
#     table_number = 0
#     team = []
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

