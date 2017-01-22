"""
    Sends a test email
"""

from hackfsu_com.util import email


def run():
    send_results = email.send_template(
        to_email='dev@hackfsu.com',
        subject='test',
        template_name='mandrill_test',
        to_first_name='Jared',
        to_last_name='Bennett',
        template_content={
            'test_data': 'Hello World!'
        }
    )

    print('Mandrill send results', send_results)
