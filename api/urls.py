from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'user/login$', views.user.LogInView.as_view(), name='user-login'),
    url(r'hackathon/subscribe$', views.hackathon.SubscribeView.as_view(), name='hackathon-subscribe')
]

if settings.DEBUG:
    urlpatterns.extend([

    ])
