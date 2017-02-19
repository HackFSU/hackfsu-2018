"""hackfsu_com URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import RedirectView
from . import views


def static_redirect(path):
    """ Serves static file """
    return RedirectView.as_view(url=settings.STATIC_URL + path)

urlpatterns = [
    # Static Website Pages
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^help$', views.HelpPage.as_view(), name='help'),

    url(r'^registration/user/$', views.registration.UserRegistrationPage.as_view(), name='registration-user'),
    url(r'^registration/hacker/$', views.registration.HackerRegistrationPage.as_view(), name='registration-hacker'),
    url(r'^registration/judge/$', views.registration.JudgeRegistrationPage.as_view(), name='registration-judge'),
    url(r'^registration/mentor/$', views.registration.MentorRegistrationPage.as_view(), name='registration-mentor'),
    url(r'^registration/organizer/$', views.registration.OrganizerRegistrationPage.as_view(),
        name='registration-organizer'),

    url(r'^user/login/$', views.user.LoginPage.as_view(), name='user-login'),
    url(r'^user/logout/$', views.user.logout_view, name='user-logout'),
    url(r'^user/profile/$', views.user.ProfilePage.as_view(), name='user-profile'),
    url(r'^user/rsvp/$', views.user.RsvpPage.as_view(), name='user-rsvp'),
    url(r'^user/password/reset/$', views.user.password.StartResetPage.as_view()),
    url(r'^user/password/reset/(?P<link_key>[A-Za-z0-9]{64})/$', views.user.password.CompleteResetPage.as_view()),

    url(r'^hype/$', views.hype.HypeIndex.as_view()),
    url(r'^hype/registration$', views.hype.HypeRegistration.as_view()),

    url(r'^judge/$', views.judge.IndexPage.as_view()),
    url(r'^judge/hack/(?P<id>\d+)/$', views.judge.HackPage.as_view()),

    url(r'^organize/$', views.organize.IndexPage.as_view()),
    url(r'^organize/attendees/$', views.organize.AttendeesPage.as_view()),
    url(r'^organize/judging/expo/$', views.organize.judging.ExpoPage.as_view()),

    url(r'^mentor/$', views.mentor.IndexPage.as_view()),
    url(r'^mentor/request/(?P<id>\d+)/$', views.mentor.RequestPage.as_view()),

    url(r'^links/$', views.LinksPage.as_view()),

    url(r'^hacks/$', views.HacksPage.as_view()),

    # Shortcuts
    url(r'^register/$', RedirectView.as_view(url='/registration/user')),
    url(r'^register/hacker/$', RedirectView.as_view(url='/registration/user?attendee_type=hacker')),
    url(r'^register/organizer/$', RedirectView.as_view(url='/registration/user?attendee_type=organizer')),
    url(r'^register/mentor/$', RedirectView.as_view(url='/registration/user?attendee_type=mentor')),
    url(r'^register/judge$', RedirectView.as_view(url='/registration/user?attendee_type=judge')),
    url(r'^login/$', RedirectView.as_view(url='/user/login')),
    url(r'^logout/$', RedirectView.as_view(url='/user/logout'))
]

if settings.DEBUG:
    urlpatterns.extend([
        # Special root-only static files handled by Apache
        url('^favicon.ico$', static_redirect('img/favicon/favicon.ico')),
        url('^browserconfig.xml$', static_redirect('img/favicon/browserconfig.xml')),

        # Error Pages
        url(r'^error/404/$', views.handler404),
        url(r'^error/500/$', views.handler500),

        # Test Pages
        url(r'^test/captcha/$', views.test.CaptchaTestPage.as_view())
    ])


