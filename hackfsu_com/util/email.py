"""
    Send transactional emails via Mailchimp's Mandrill client
"""

from hackfsu_com import keys
import mandrill
import logging

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

    if template_name not in templates:
        raise ValueError('Invalid template name or template unknown')

    # Automatically add first and last name to context
    merge_vars = MandrillContent(merge_vars if merge_vars is not None else {})
    template_content = MandrillContent(template_content if template_content is not None else {})

    # Defaults
    if 'first_name' not in merge_vars:
        merge_vars['first_name'] = to_first_name
    if 'last_name' not in merge_vars:
        merge_vars['last_name'] = to_last_name

    message = {
        'subject': subject,
        'from_email': default_from_email,
        'from_name': default_from_name,
        'to': [{
            'email': to_email,
            'name': to_first_name + ' ' + to_last_name
        }],
        'global_merge_vars': global_merge_vars.list(),
        'merge_vars': [{
            'rcpt': to_email,
            'vars': merge_vars.list()
        }]
    }

    send_results = mandrill_client.messages.send_template(
        template_name=template_name, template_content=template_content.list(), message=message
    )

    for result in send_results:
        if result['status'] != 'sent':
            logging.info('Unable to send email. Mandrill result: ' + str(result))

    return send_results


