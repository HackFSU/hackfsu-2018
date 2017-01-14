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
    # Special root-only static files
    url('^favicon.ico$', static_redirect('img/favicon/favicon.ico')),
    url('^browserconfig.xml$', static_redirect('img/favicon/browserconfig.xml')),

    # Static Website Pages
    url(r'^$', views.IndexPage.as_view(), name='index'),
    # url(r'^help$', views.HelpPage.as_view(), name='help'),

    url(r'^registration/hacker/$', views.registration.HackerRegistrationPage.as_view(), name='registration-hacker'),
    # url(r'^registration/judge/$', views.registration.JudgeRegistrationPage.as_view(), name='registration-judge'),
    # url(r'^registration/mentor/$', views.registration.MentorRegistrationPage.as_view(), name='registration-mentor'),
    # url(r'^registration/organizer/$', views.registration.OrganizerRegistrationPage.as_view(),
    #     name='registration-organizer'),

    # url(r'^user/login/$', views.user.LoginPage.as_view(), name='user-login'),
    # url(r'^user/profile/$', views.user.ProfilePage.as_view(), name='user-profile')
]

if settings.DEBUG:
    urlpatterns.extend([
        url(r'^error/404/$', views.handler404),
        url(r'^error/500/$', views.handler500),
    ])


