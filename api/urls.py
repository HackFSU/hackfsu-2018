from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'user/login$', views.user.LogInView.as_view()),
    url(r'hackathon/subscribe$', views.hackathon.SubscribeView.as_view())
]

if settings.DEBUG:
    urlpatterns.extend([

    ])
