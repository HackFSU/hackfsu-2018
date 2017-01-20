from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'user/login$', views.user.LogInView.as_view(), name='user-login'),
    url(r'user/get/profile$', views.user.ProfileView.as_view(), name='user-get-profile'),
    url(r'user/register$', views.user.RegisterView.as_view(), name='user-register'),

    url(r'hacker/register$', views.hacker.RegisterView.as_view(), name='hacker-register'),

    url(r'judge/register$', views.judge.RegisterView.as_view(), name='judge-register'),

    url(r'mentor/register$', views.hacker.RegisterView.as_view(), name='mentor-register'),

    url(r'organizer/register$', views.hacker.RegisterView.as_view(), name='organizer-register'),

    url(r'school/get', views.school.GetView.as_view(), name='organizer-register')
]

if settings.DEBUG:
    urlpatterns.extend([

    ])
