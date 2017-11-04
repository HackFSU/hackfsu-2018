"""
    Get public statistics for current hackathon
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import Hackathon, HackerInfo, MentorInfo, JudgeInfo, OrganizerInfo, AttendeeStatus
from django.utils import timezone


class ResponseForm(forms.Form):
    hackathon_name = forms.CharField()
    hackathon_start = forms.DateField()
    hackathon_end = forms.DateField()
    hackers_registered = forms.IntegerField()
    hackers_approved = forms.IntegerField()
    hackers_rsvp = forms.IntegerField()
    hackers_checked_in = forms.IntegerField()
    mentors_registered = forms.IntegerField()
    mentors_approved = forms.IntegerField()
    mentors_rsvp = forms.IntegerField()
    mentors_checked_in = forms.IntegerField()
    judges_registered = forms.IntegerField()
    judges_approved = forms.IntegerField()
    judges_rsvp = forms.IntegerField()
    judges_checked_in = forms.IntegerField()
    organizers_registered = forms.IntegerField()
    organizers_approved = forms.IntegerField()
    organizers_rsvp = forms.IntegerField()
    organizers_checked_in = forms.IntegerField()


class StatsView(ApiView):
    response_form_class = ResponseForm
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_user])

    def work(self, request, req: dict, res: dict):
        ch = Hackathon.objects.current()

        res['hackathon_name'] = ch.name
        res['hackathon_start'] = ch.start_date
        res['hackathon_end'] = ch.end_date

        if (timezone.now().date() - ch.start_date).days >= 0 or \
                OrganizerInfo.objects.filter(hackathon=ch, user=request.user, approved=True).exists():

            res['hackers_registered'] = HackerInfo.objects.filter(hackathon=ch).count()
            res['hackers_approved'] = HackerInfo.objects.filter(hackathon=ch, approved=True).count()
            res['hackers_rsvp'] = \
                HackerInfo.objects.filter(hackathon=ch, approved=True, attendee_status__rsvp_result=1).count()
            res['hackers_checked_in'] = HackerInfo.objects.filter(
                hackathon=ch, approved=True, attendee_status__checked_in_at__isnull=False).count()

            res['mentors_registered'] = MentorInfo.objects.filter(hackathon=ch).count()
            res['mentors_approved'] = MentorInfo.objects.filter(hackathon=ch, approved=True).count()
            res['mentors_rsvp'] = \
                MentorInfo.objects.filter(hackathon=ch, approved=True, attendee_status__rsvp_result=1).count()
            res['mentors_checked_in'] = MentorInfo.objects.filter(
                hackathon=ch, approved=True, attendee_status__checked_in_at__isnull=False).count()

            res['judges_registered'] = JudgeInfo.objects.filter(hackathon=ch).count()
            res['judges_approved'] = JudgeInfo.objects.filter(hackathon=ch, approved=True).count()
            res['judges_rsvp'] = \
                JudgeInfo.objects.filter(hackathon=ch, approved=True, attendee_status__rsvp_result=1).count()
            res['judges_checked_in'] = JudgeInfo.objects.filter(
                hackathon=ch, approved=True, attendee_status__checked_in_at__isnull=False).count()

            res['organizers_registered'] = OrganizerInfo.objects.filter(hackathon=ch).count()
            res['organizers_approved'] = OrganizerInfo.objects.filter(hackathon=ch, approved=True).count()
            res['organizers_rsvp'] = \
                OrganizerInfo.objects.filter(hackathon=ch, approved=True, attendee_status__rsvp_result=1).count()
            res['organizers_checked_in'] = OrganizerInfo.objects.filter(
                hackathon=ch, approved=True, attendee_status__checked_in_at__isnull=False).count()

        else:
            res['hackers_registered'] = -1
            res['hackers_approved'] = -1
            res['hackers_rsvp'] = -1
            res['hackers_checked_in'] = -1
            res['mentors_registered'] = -1
            res['mentors_approved'] = -1
            res['mentors_rsvp'] = -1
            res['mentors_checked_in'] = -1
            res['judges_registered'] = -1
            res['judges_approved'] = -1
            res['judges_rsvp'] = -1
            res['judges_checked_in'] = -1
            res['organizers_registered'] = -1
            res['organizers_approved'] = -1
            res['organizers_rsvp'] = -1
            res['organizers_checked_in'] = -1
