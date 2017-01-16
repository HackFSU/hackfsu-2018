
from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl


class ResponseForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()


class ProfileView(ApiView):
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_user])
    response_form_class = ResponseForm

    def work(self, request, req, res):
        res['first_name'] = request.user.first_name
        res['last_name'] = request.user.last_name
        res['email'] = request.user.email
