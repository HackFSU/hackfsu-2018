"""
    Basic exception with custom utility functions
"""

from hackfsu_com.util import email
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import logging
import traceback


def get_admin_email_recipients() -> list:
    recipients = list()
    recipients.append({
        'email'
    })

    admins = User.objects.filter(sta)

    return recipients


def email_log_html(title: str, code: str) -> str:
    return '<h2><b>{}</b></h2><p style="font-family: Courier">{}</p><br>'.format(
        title, code
    )


class BaseError(Exception):
    response_status = 500

    def __init__(self, source_exception: Exception):
        if source_exception is not None:
            if not isinstance(source_exception, Exception):
                raise TypeError('Invalid source_exception. Must be an Exception')
            self.message = str(source_exception)
        else:
            source_exception = Exception()

        self.cause = source_exception
        self.message = str(source_exception)
        self.stack_trace = traceback.format_exc()

    def email_log_to_dev(self, request_info: str, user=None):
        html_str = '<h1><b>Internal Server Error Detected!</b></h1><br>'

        if user is not None and not user.is_anonymous:
            html_str += '<h2><b>Caused by User</b></h2><p>Name: {} {}<br>Email: {}<br>Groups: {}</p><br>'.format(
                user.first_name, user.last_name,
                user.email,
                ', '.join(list(user.groups.values_list('name', flat=True)))
            )
        else:
            html_str += '<h2><b>Caused by Anonymous User</b></h2>'

        html_str += email_log_html(
            title='Error Information:',
            code=email.str_to_html_str(
                '\tError Type: {}\n\tError Message: {}\n\tStack Trace: {}'.format(
                    self.cause.__class__.__name__, self.message, self.stack_trace
                )
            )
        )

        html_str += email_log_html(
            title='Response Information:',
            code=email.str_to_html_str(request_info)
        )

        merge_vars = email.MandrillContent()
        merge_vars['html_content'] = html_str
        send_results = email.email_recipients(
            template_name='standard_html',
            extra_global_merge_vars=merge_vars.list(),
            to=email.get_admins_email_to(),
            subject='Server Error Report: ' + self.cause.__class__.__name__
        )

        logging.warning('Error notification emails send results: ' + str(send_results))

    def log(self):
        logging.error(self.__class__.__name__, exc_info=True, )

    def json_response(self, include_message=True) -> JsonResponse:
        response = self.to_dict()

        if not include_message:
            del response['message']

        return JsonResponse(response, status=self.response_status)

    def to_dict(self):
        return {
            'error': _(self.__class__.__name__),
            'cause': _(self.cause.__class__.__name__),
            'message': self.message
        }

    def __str__(self):
        return str(self.to_dict())
