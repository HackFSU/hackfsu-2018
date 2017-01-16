"""
    Logs user with the given credentials in for the stored session
"""
from django import forms
from hackfsu_com.views.generic import ApiView
from django.db import models


class RequestForm(forms.Form):
    email = forms.EmailField(required=True, max_length=100)


class SubscribeView(ApiView):
    request_form_class = RequestForm

    def work(self, request, req, res):
        subscriber = models.Subscriber.objects.create(
            email=req['email'],
            hackathon=models.Hackathon.objects.current())
        subscriber.full_clean()
        subscriber.save()
