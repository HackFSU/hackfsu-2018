from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from . import settings


def static_redirect(path):
    """ Serves static file """
    return RedirectView.as_view(url=settings.STATIC_URL + path)


def index(request):
    return render(request, 'index/index.html')
