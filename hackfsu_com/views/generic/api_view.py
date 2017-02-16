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
from hackfsu_com.util.exceptions import InternalServerError, ExternalUserError
import logging


def format_request_info(request: HttpRequest, input_data: dict, req, res):
    return '\tRequest: {}\n\tRaw Input: {}\n\tReq: {}\n\tRes: {}'.format(
        str(request), str(input_data), str(req), str(res)
    )


class ApiView(View):
    http_method_names = ['post']        # Override to allow GET
    request_form_class = forms.Form     # Override each time
    response_form_class = forms.Form    # Override each time
    access_manager = acl.AccessManager()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = list()
        self.args = list()

    def get(self, request: HttpRequest,  *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self.process(request, request.GET)

    def post(self, request: HttpRequest, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self.process(request, request.POST)

    def process(self, request: HttpRequest, input_data: dict):
        """ Validates input and attempts to preform work() logic. Returns the correct JsonResponse """

        # Authenticate Access
        if not self.authenticate(request):
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
                raise ExternalUserError(ValidationError(request_form.errors.as_data()))
            req = request_form.cleaned_data
            res = {}

            # Preform desired api task and populate response (res) object
            try:
                self.work(request, req, res)
            except ValidationError as e:
                raise ExternalUserError(e)

            # Validate response
            response_form = self.response_form_class(res)
            if not response_form.is_valid():
                raise InternalServerError(ValidationError(response_form.errors.as_data()))
            res = response_form.cleaned_data

            # Successful api call!
            return JsonResponse(res)

        except ExternalUserError as error:
            if settings.DEBUG:
                logging.error(format_request_info(request, input_data, res, req))
                error.log()
            return error.json_response()
        except InternalServerError as error:
            request_info = format_request_info(request, input_data, res, req)
            logging.error(request_info)
            error.log()

            if not settings.DEBUG:
                error.email_log_to_dev(request_info=request_info, user=request.user)

            return error.json_response(include_message=False)
        except Exception as e:
            error = InternalServerError(e)
            request_info = format_request_info(request, input_data, res, req)
            logging.error(request_info)
            error.log()

            if not settings.DEBUG:
                error.email_log_to_dev(request_info=request_info, user=request.user)

            return error.json_response(include_message=False)

    def work(self, request: HttpRequest, req: dict, res: dict):
        """
            Preforms api request logic
            :param request Django request object (only use this if necessary)
            :param req cleaned and valid request data
            :param res response data to be checked after this call
        """
        pass

    def authenticate(self, request):
        """ To be overridden if necessary. Should still be called with super """
        return self.access_manager.check_user(request.user)
