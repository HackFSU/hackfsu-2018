from django.conf.urls import url
from django.conf import settings
from . import views
urlpatterns = [
    url(r'hackathon/get/countdowns$', views.hackathon.get.CountdownsView.as_view()),
    url(r'hackathon/get/maps$', views.hackathon.get.MapsView.as_view()),
    url(r'hackathon/get/schedule_items$', views.hackathon.get.ScheduleItemsView.as_view()),
    url(r'hackathon/get/sponsors$', views.hackathon.get.SponsorsView.as_view()),
    url(r'hackathon/get/updates$', views.hackathon.get.UpdatesView.as_view()),
    url(r'hackathon/get/stats$', views.hackathon.get.StatsView.as_view()),
    url(r'hackathon/get/prizes$', views.hackathon.get.PrizesView.as_view()),
    url(r'hackathon/get/csv/attendees_checked_in$', views.hackathon.get.csv.AttendeesCheckedInCsv.as_view()),

    url(r'user/login$', views.user.LogInView.as_view(), name='user-login'),
    # url(r'user/register$', views.user.RegisterView.as_view(), name='user-register'),
    url(r'user/get/profile$', views.user.get.ProfileView.as_view(), name='user-get-profile'),
    url(r'user/get/groups$', views.user.get.GroupsView.as_view(), name='user-get-groups'),
    url(r'user/password/reset/complete$', views.user.password.CompleteResetView.as_view()),
    url(r'user/password/reset/start$', views.user.password.StartResetView.as_view()),

    url(r'hacker/register$', views.hacker.RegisterView.as_view(), name='hacker-register'),
    url(r'hacker/get/profile$', views.hacker.get.ProfileView.as_view(), name='hacker-get-profile'),
    url(r'hacker/get/csv/by_school$', views.hacker.get.csv.BySchoolCsv.as_view()),
    url(r'hacker/get/csv/resume_links$', views.hacker.get.csv.ResumeLinksCsv.as_view()),

    url(r'judge/register$', views.judge.RegisterView.as_view(), name='judge-register'),
    url(r'judge/assign_hacks$', views.judge.AssignHacksView.as_view()),
    url(r'judge/get/approved_and_checked_in$', views.judge.get.ApprovedAndCheckedInView.as_view()),
    url(r'judge/get/grades$', views.judge.get.GradesView.as_view()),
    url(r'judge/get/hack_with_criteria$', views.judge.get.HackWithCriteriaView.as_view()),
    url(r'judge/get/hacks_with_criteria$', views.judge.get.HacksWithCriteriaView.as_view()),
    url(r'judge/get/pending_hack_assignments$', views.judge.get.PendingHackAssignmentView.as_view()),
    url(r'judge/get/csv/hacks_with_manual_criteria$', views.judge.get.csv.HacksWithManualCriteriaCsv.as_view()),
    url(r'judge/assignment/cancel$', views.judge.assignment.CancelView.as_view()),
    url(r'judge/assignment/submit_grades$', views.judge.assignment.SubmitGradesView.as_view()),
    url(r'judge/get/profile$', views.judge.get.ProfileView.as_view(), name='judge-get-profile'),

    url(r'mentor/register$', views.mentor.RegisterView.as_view(), name='mentor-register'),
    url(r'mentor/get/profile$', views.mentor.get.ProfileView.as_view(), name='mentor-get-profile'),
    url(r'mentor/request/create$', views.mentor.request.CreateView.as_view()),
    url(r'mentor/request/claim$', views.mentor.request.ClaimView.as_view()),
    url(r'mentor/request/release_claim$', views.mentor.request.ReleaseClaimView.as_view()),
    url(r'mentor/request/get/$', views.mentor.request.get.AllView.as_view()),
    url(r'mentor/request/get/id/(?P<id>\d+)$', views.mentor.request.get.SingleView.as_view()),

    url(r'organizer/register$', views.organizer.RegisterView.as_view(), name='organizer-register'),
    url(r'organizer/get/profile$', views.organizer.get.ProfileView.as_view(), name='organizer-get-profile'),
    url(r'organizer/get/csv/roster$', views.organizer.get.csv.RosterCsv.as_view()),

    url(r'school/get$', views.school.GetView.as_view(), name='organizer-register'),

    url(r'attendee/rsvp$', views.attendee.RsvpView.as_view()),
    url(r'attendee/check_in$', views.attendee.CheckInView.as_view()),
    url(r'attendee/assign_wifi_credentials$', views.attendee.AssignWifiCredentialsView.as_view()),
    url(r'attendee/get/approved_full$', views.attendee.get.ApprovedFullView.as_view()),

    url(r'preview/register$', views.preview.RegisterView.as_view(), name='preview-register'),
]


if settings.DEBUG:
    urlpatterns.extend([

    ])
