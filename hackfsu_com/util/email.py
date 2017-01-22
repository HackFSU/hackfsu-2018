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
    'user-registered',
    'hacker-register-waiting',
    'hacker-register-accepted',
    'judge-register-waiting',
    'judge-register-accepted',
    'mentor-register-waiting',
    'mentor-register-accepted',
    'organizer-register-waiting',
    'organizer-register-accepted',
    'mandrill_test'
]

default_from_email = 'noreply@hackfsu.com'
default_from_name = 'HackFSU Team'


class TemplateContentList(list):
    def add_default(self, name, content):
        if name not in self:
            self.append({
                'name': name,
                'content':  content
            })


def send_template(to_email, to_first_name, to_last_name, template_name, subject, template_content=None):
    """ Template sending wrapper for ease of use """

    if template_name not in templates:
        raise ValueError('Invalid template name or template unknown')

    # Automatically add first and last name to context
    if template_content is None:
        template_content = {}
    elif template_content is not dict:
        ValueError('template_content must be dict')
    if 'first_name' not in template_content:
        template_content['first_name'] = to_first_name
    if 'last_name' not in template_content:
        template_content['last_name'] = to_last_name

    # Convert template dict to array for mandrill
    template_content_list = []
    for key in template_content.keys():
        template_content_list.append({
            'name': key,
            'content': template_content[key]
        })

    message = {
        'subject': subject,
        'from_email': default_from_email,
        'from_name': default_from_name,
        'to': [{
            'email': to_email,
            'name': to_first_name + ' ' + to_last_name
        }]
    }

    send_results = mandrill_client.messages.send_template(
        template_name=template_name, template_content=template_content_list, message=message
    )

    for result in send_results:
        if result['status'] != 'sent':
            logging.info('Unable to send email. Mandrill result: ' + str(result))

    return send_results


