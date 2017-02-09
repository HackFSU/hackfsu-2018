from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from hackfsu_com.util import acl
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class AttendeeStatusManager(models.Manager):
    @staticmethod
    def get_or_create(user: User, hackathon: Hackathon):
        """ Gets current attendee status for user/hackathon combo. If non exists one is created properly """
        try:
            attendee_status = AttendeeStatus.objects.get(user=user, hackathon=hackathon)
        except ObjectDoesNotExist:
            attendee_status = AttendeeStatus.objects.create(user=user, hackathon=hackathon)
            acl.add_user_to_group(user, acl.group_attendee)
        return attendee_status


class AttendeeStatus(models.Model):
    objects = AttendeeStatusManager()

    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)

    comments = models.CharField(max_length=1000, default='', blank=True)    # Written by an admin manually if needed
    extra_info = models.CharField(max_length=500, default='', blank=True)   # User submitted in RSVP

    rsvp_email_sent_at = models.DateTimeField(null=True, blank=True)    # We asked them to rsvp
    rsvp_submitted_at = models.DateTimeField(null=True, blank=True)     # They have submitted the RSVP form
    rsvp_result = models.BooleanField(default=False)                    # True = Going, False = Not Going
    checked_in_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '[{} {}\'s Attendee Status]'.format(self.user.first_name, self.user.last_name)


@receiver(pre_delete, sender=AttendeeStatus)
def on_pre_delete(**kwargs):
    """ Update base user class's groups """
    instance = kwargs['instance']
    if instance.hackathon == Hackathon.objects.current():
        acl.remove_user_from_group(instance.user, acl.group_attendee)


class CheckedInFilter(admin.SimpleListFilter):
    title = 'Checked in'
    parameter_name = 'checked_in_at'

    def lookups(self, request, model_admin):
        return (
            ('1', 'No'),
            ('0', 'Yes')
        )

    def queryset(self, request, queryset):
        if self.value() in ('0', '1'):
            kwargs = {'{}__isnull'.format(self.parameter_name): self.value() == '1'}
            return queryset.filter(**kwargs)
        return queryset


@admin.register(AttendeeStatus, site=hackfsu_admin)
class AttendeeStatusAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'rsvp_result', CheckedInFilter)
    list_display = ('id', 'user_info', 'created', 'rsvp_email_sent_at',
                    'rsvp_submitted_at', 'checked_in_at', 'comments', 'extra_info')
    list_editable = ('comments',)
    list_display_links = ('id',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'comments')
    ordering = ('-created',)

    @staticmethod
    def user_info(obj):
        return "{} {} - {}".format(obj.user.first_name, obj.user.last_name, obj.user.email)
