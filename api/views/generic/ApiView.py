"""
    Generic base class for API calls using forms for input validation

    Returns a JsonResponse with varying status codes for error handling.

    TODO user group authentication support
    TODO sensitive parameter support
"""

from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.generic import View
from django.utils.translation import ugettext as _
from django import forms
from django.conf import settings


class ApiView(View):
    http_method_names = ['post']        # Override to allow GET
    request_form_class = forms.Form     # Override each time
    response_form_class = forms.Form    # Override each time

    def get(self, request):
        return self.process(request, request.GET)

    def post(self, request):
        return self.process(request, request.POST)

    def process(self, request, input_data):
        """ Validates input and attempts to preform work() logic. Returns the correct JsonResponse """
        try:
            # Validate & clean request
            request_form = self.request_form_class(input_data, request.FILES)
            if not request_form.is_valid():
                raise ValidationError(request_form.errors.as_data())
            req = request_form.cleaned_data
            res = {}

            # Preform desired api task and populate response (res) object
            self.work(request, req, res)

            # Validate response
            response_form = self.response_form_class(res)
            if not response_form.is_valid():
                raise ValidationError(response_form.errors.as_data())

            # Successful api call!
            return JsonResponse(response_form.cleaned_data)

        except ValidationError as e:
            return JsonResponse({
                'message': _('Validation Error: '),
                'cause': str(e)
            }, status=400)
        except Exception as e:
            error_data = {'message': _('Internal Server Error')}
            if settings.DEBUG:
                error_data['cause'] = str(e)
            return JsonResponse(error_data, status=500)

    def work(self, request, req, res):
        """
            Preforms api request logic
            :param request Django request object (only use this if necessary)
            :param req cleaned and valid request data
            :param res response data to be checked after this call
        """
        pass
