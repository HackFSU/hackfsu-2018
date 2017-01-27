"""
    Send transactional emails via Mailchimp's Mandrill client
"""

from django.contrib.auth.models import User
from hackfsu_com import keys
import mandrill
import logging
import re

mandrill_client = mandrill.Mandrill(
    apikey=keys.MANDRILL_API_KEY
)

# List of templates known to exist in MailChimp
templates = [
    'user_registered',
    'hacker_register_waiting',
    'hacker_register_accepted',
    'judge_register_waiting',
    'judge_register_accepted',
    'mentor_register_waiting',
    'mentor_register_accepted',
    'organizer_register_waiting',
    'organizer_register_accepted',
    'mandrill_test',
    'standard_html'
]

default_from_email = 'noreply@hackfsu.com'
default_from_name = 'HackFSU Team'


class MandrillContent(dict):
    def list(self):
        content_list = []
        for key in self.keys():
            content_list.append({
                'name': key,
                'content': self[key]
            })
        return content_list

global_merge_vars = MandrillContent()


def send_template(to_email, to_first_name, to_last_name, template_name, subject, merge_vars=None,
                  template_content=None):
    """ Template sending wrapper for ease of use """

    # Automatically add first and last name to context
    merge_vars = MandrillContent(merge_vars if merge_vars is not None else {})

    # Defaults
    if 'first_name' not in merge_vars:
        merge_vars['first_name'] = to_first_name
    if 'last_name' not in merge_vars:
        merge_vars['last_name'] = to_last_name

    to = [{
        'email': to_email,
        'name': to_first_name + ' ' + to_last_name
    }]

    return email_recipients(
        template_name=template_name,
        template_content=template_content,
        extra_global_merge_vars=merge_vars.list(),
        subject=subject,
        to=to,
    )


def email_recipients(template_name: str, subject: str, to: list, extra_global_merge_vars=list(), merge_vars=list(),
                     template_content=None):
    """ Template sending wrapper for ease of use """

    if template_name not in templates:
        raise ValueError('Invalid template name or template unknown')

    # Automatically add first and last name to context
    template_content = MandrillContent(template_content if template_content is not None else {})
    g_merge_vars = list()
    g_merge_vars.extend(global_merge_vars.list())
    g_merge_vars.extend(extra_global_merge_vars)

    message = {
        'subject': subject,
        'from_email': default_from_email,
        'from_name': default_from_name,
        'to': to,
        'global_merge_vars': g_merge_vars,
        'merge_vars': merge_vars
    }

    send_results = mandrill_client.messages.send_template(
        template_name=template_name, template_content=template_content.list(), message=message
    )

    for result in send_results:
        if result['status'] != 'sent':
            logging.error('Unable to send email. Mandrill result: ' + str(result))

    return send_results


def str_to_html_str(base_string: str) -> str:
    # Handle space indents
    base_string = re.sub(r'^[ ]*([ ])+', repl='&nbsp;', string=base_string, flags=re.MULTILINE)
    base_string = re.sub(r'^[\t]*([ \t])+', repl='&nbsp;&nbsp;&nbsp;&nbsp;', string=base_string, flags=re.MULTILINE)
    base_string = re.sub(r'\n', repl='<br>', string=base_string)
    return base_string


def get_admins_email_to() -> list:
    recipients = list()
    recipients.append({
        'type': 'to',
        'email': keys.ADMIN_EMAIL,
        'name': 'System Administrator'
    })

    admins = User.objects.filter(is_superuser=True)
    for admin in admins:
        recipients.append({
            'type': 'cc',
            'name': admin.first_name + ' ' + admin.last_name,
            'email': admin.email
        })

    return recipients
