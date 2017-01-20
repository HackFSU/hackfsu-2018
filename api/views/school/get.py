"""
    Returns list of all schools
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import School


class ResponseForm(forms.Form):
    school_choices = forms.Field()      # [{id: "", name: ""}]


class GetView(ApiView):
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_deny=[acl.group_user])

    def work(self, request: HttpRequest, req: dict, res: dict):
        schools = School.objects.all()
        school_data = list()
        for s in schools:
            school_data.append({
                'id': s.id,
                'name': s.name
            })

        res['school_choices'] = school_data
