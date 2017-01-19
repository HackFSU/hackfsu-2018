"""
    Send transactional emails via Mailchimp's Mandrill client
"""

from hackfsu_com import keys
import mandrill

mandrill_client = mandrill.Mandrill(keys.MANDRILL_API_KEY)

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
    'organizer-register-accepted'
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
        template_content = []

    t_content = TemplateContentList(template_content)
    t_content.add_default('first_name', to_first_name)
    t_content.add_default('last_name', to_last_name)

    message = {
        'to': [{
            'email': to_email,
            'name': to_first_name + ' ' + to_last_name
        }],
        'message': {
            'subject': subject,
            'from_email': default_from_email,
            'from_name': default_from_name
        }
    }

    return mandrill_client.messages.send_template(template_name=template_name, template_content=list(t_content),
                                                  message=message)
