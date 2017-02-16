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


@admin.register(HelpRequest, site=hackfsu_admin)
class HelpRequestAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('id', 'created', 'assigned_mentor_info', 'attendee_name', 'request')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('attendee_name', 'location', 'description')
    ordering = ('-created',)

    @staticmethod
    def assigned_mentor_info(obj):
        return "{} {} - {}".format(obj.assigned_mentor.first_name, obj.assigned_mentor.last_name,
                                   obj.assigned_mentor.email)
