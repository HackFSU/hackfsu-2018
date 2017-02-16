from django.db import models
from api.models import Hackathon, MentorInfo
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class HelpRequest(models.Model):

    LOCATION_FLOORS = (
        (1, 'Basement'),
        (2, 'Entrance Floor'),
        (3, 'Upper Floor')
    )

    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    assigned_mentor = models.ForeignKey(to=MentorInfo, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    location_x = models.PositiveSmallIntegerField()  # Percentage
    location_y = models.PositiveSmallIntegerField()  # Percentage
    location_floor = models.PositiveSmallIntegerField(choices=LOCATION_FLOORS)
    attendee_name = models.CharField(max_length=100)
    attendee_description = models.CharField(max_length=100)
    request = models.CharField(max_length=1000)

    def __str__(self):
        return '[HelpRequest @ {}]'.format(self.created)

    def json(self, check_user):
        r = {
            'id': self.id,
            'location': {
                'floor': self.location_floor,
                'x': self.location_x,
                'y': self.location_y
            },
            'attendee': {
                'name': self.attendee_name,
                'description': self.attendee_description
            },
            'request': self.request
        }

        if self.assigned_mentor is not None:
            user = self.assigned_mentor.user
            r['assigned_mentor'] = {
                'name': '{} {}'.format(user.first_name, user.last_name),
                'is_me': user.id == check_user.id
            }
        return r


class ClaimedFilter(admin.SimpleListFilter):
    title = 'Claimed'
    parameter_name = 'assigned_mentor'

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


@admin.register(HelpRequest, site=hackfsu_admin)
class HelpRequestAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', ClaimedFilter)
    list_display = ('id', 'assigned_mentor_info', 'attendee_name', 'request', 'location_floor', 'created')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('attendee_name', 'location', 'description')
    ordering = ('-created',)

    @staticmethod
    def assigned_mentor_info(obj):
        if obj.assigned_mentor is not None:
            return "{} {} - {}".format(
                obj.assigned_mentor.user.first_name,
                obj.assigned_mentor.user.last_name,
                obj.assigned_mentor.user.email
            )
        else:
            return '<unclaimed>'
