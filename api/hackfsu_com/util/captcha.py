"""
    Google reCAPTCHA validation
"""
from django.conf import settings

from hackfsu_com import keys
import requests
import json
import logging

GOOGLE_VERIFICATION_URL = "https://www.google.com/recaptcha/api/siteverify"


def is_valid_response(g_recaptcha_response: str) -> bool:

    if settings.DEBUG:
        return True

    """ Sends a request to google and checks the captcha response for validity """
    response = requests.post(GOOGLE_VERIFICATION_URL, data={
        'secret': keys.RECAPTCHA_SECRET,
        'response': g_recaptcha_response
    })
    try:
        json_response = json.loads(response.text)
    except ValueError:
        logging.exception('Unable to parse reCaptcha verification response')
        return False
    if json_response['success']:
        return True
    else:
        logging.warning('Captcha Failure: ' + str(json_response))
        return False


