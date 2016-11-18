from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [

]

if settings.DEBUG:
    urlpatterns.extend([
        url(r'debug/test', views.debug.test),
        url(r'debug/save', views.debug.save)
    ])
