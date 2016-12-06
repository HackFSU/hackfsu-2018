from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [

]

if settings.DEBUG:
    urlpatterns.extend([
        url(r'hackathon/subscribe$', views.hackathon.subscribe)
    ])
