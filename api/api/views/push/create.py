"""
    Proxy a new push notification to the push service
    and then gorush. Maybe save as update.
"""

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util.forms import JsonField
from hackfsu_com.util import acl
from api.models import HackathonUpdate, Hackathon

import requests

class CreatePushView(ApiView):
    class RequestForm(forms.Form):
        title = forms.CharField()
        body = forms.CharField()
        isUpdate = forms.IntegerField()

    http_method_names = ['post']
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])

    def work(self, request, req, res):
        url = "{}/push/new".format(settings.PUSH_HOST)
        payload = {
            'title': req['title'],
            'message': req['body']
        }
        resp = requests.post(url, json=payload)


        # Optional save as HackathonUpdate
        if req['isUpdate'] is 1:
            update = HackathonUpdate(
                hackathon=Hackathon.objects.current(),
                title=req['title'],
                content=req['body']
            )
            update.save()
