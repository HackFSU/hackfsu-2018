"""
    Returns list of all schools.
"""
from django import forms
from django.http.request import HttpRequest
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util.forms import JsonField
from hackfsu_com.util import acl
from api.models import School


class RequestForm(forms.Form):
    include_user_submitted = forms.BooleanField(required=False)


class ResponseForm(forms.Form):
    school_choices = JsonField()        # [{id: "", name: ""}]


class GetView(ApiView):
    http_method_names = ['get']
    request_form_class = RequestForm
    response_form_class = ResponseForm
    # access_manager = acl.AccessManager(acl_deny=[acl.group_user])

    def work(self, request: HttpRequest, req: dict, res: dict):
        schools = []
        if req['include_user_submitted']:
            schools.extend(School.objects.all())
        else:
            schools.extend(School.objects.filter(user_submitted=False))
        school_data = list()
        for s in schools:
            school_data.append({
                'id': s.id,
                'name': s.name
            })

        res['school_choices'] = school_data
