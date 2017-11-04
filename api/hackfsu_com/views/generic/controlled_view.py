"""
    Base class for views controlled by ACL
"""

from django.http import Http404, HttpResponse
from django.views.generic import View
from django.conf import settings
from hackfsu_com.util import acl
from hackfsu_com.util.exceptions import InternalServerError
import logging


class ControlledView(View):
    http_method_names = ['post', 'get']
    access_manager = acl.AccessManager()

    def get(self, request):
        return self.pre_process(request, request.GET)

    def post(self, request):
        return self.pre_process(request, request.POST)

    def pre_process(self, request, input_data: dict):
        """ Validates input and attempts to preform work() logic. Returns the correct JsonResponse """

        # Authenticate Access
        if not self.authenticate(request):
            error_response = self.return_error_response(request)
            if error_response is None:
                raise Http404()
            return error_response
        try:
            return self.process(request, input_data)
        except Exception as e:
            error = InternalServerError(e)
            request_info = self.format_request_info(request, input_data)
            logging.error(request_info)
            error.log()

            if not settings.DEBUG:
                error.email_log_to_dev(request_info=request_info, user=request.user)

            return error.json_response(include_message=False)

    def authenticate(self, request):
        """ To be overridden if necessary. Should still be called with super """
        return self.access_manager.check_user(request.user)

    def return_error_response(self, request) -> HttpResponse:
        pass

    def process(self, request, input_data):
        pass

    @staticmethod
    def format_request_info(request, input_data):
        return '\tRequest: {}\n\tRaw Input: {}'.format(
            str(request), str(input_data)
        )
