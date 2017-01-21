"""
    Generic base class for API calls using forms for input validation

    Returns a JsonResponse with varying status codes for error handling.

    TODO user group authentication support
    TODO sensitive parameter support
"""

from django.http import JsonResponse, HttpRequest
from django.core.exceptions import ValidationError
from django.views.generic import View
from django.utils.translation import ugettext as _
from django.conf import settings
from django import forms
from hackfsu_com.util import acl
import logging


class ApiView(View):
    http_method_names = ['post']        # Override to allow GET
    request_form_class = forms.Form     # Override each time
    response_form_class = forms.Form    # Override each time
    access_manager = acl.AccessManager()

    def get(self, request: HttpRequest):
        return self.process(request, request.GET)

    def post(self, request: HttpRequest):
        return self.process(request, request.POST)

    def process(self, request: HttpRequest, input_data):
        """ Validates input and attempts to preform work() logic. Returns the correct JsonResponse """

        # Authenticate Access
        if not self.access_manager.check_user(request.user):
            return JsonResponse({
                'cause': _('Unauthorized')
            }, status=401)

        req = None
        res = None

        # Preform request
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
            res = response_form.cleaned_data

            # Successful api call!
            return JsonResponse(response_form.cleaned_data)

        except ValidationError as e:
            if settings.DEBUG:
                logging.error(
                    'Validation Error\n\tRequest: {}\n\tRaw Input: {}\n\tReq: {}\n\tRes: {}\n\tError: {}'.format(
                        str(request), str(input_data.dict()), str(req), str(res), str(e.message_dict)
                    )
                )

            return JsonResponse({
                'cause': _('Validation Error'),
                'message': e.message_dict
            }, status=400)
        except Exception as e:
            error_data = {'cause': _('Internal Server Error')}
            logging.exception('Internal Server Error ' + str(request))
            return JsonResponse(error_data, status=500)

    def work(self, request: HttpRequest, req: dict, res: dict):
        """
            Preforms api request logic
            :param request Django request object (only use this if necessary)
            :param req cleaned and valid request data
            :param res response data to be checked after this call
        """
        pass
