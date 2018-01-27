"""

Accessor for private keys in the environment

"""
import os
import json

APP_DEBUG = str(os.getenv('APP_DEBUG')).lower() == 'true'

# Required secret keys
APP_SECRET = str()
DB_NAME = str()
DB_SCHEMA = str()
DB_HOST = str()
DB_PORT = str()
DB_USER = str()
DB_PASSWORD = str()
RECAPTCHA_SECRET = str()
MANDRILL_API_KEY = str()
MANDRILL_HOST = str()
MANDRILL_PORT = str()
MANDRILL_SMTP_USERNAME = str()
MANDRILL_SMTP_PASSWORD = str()
ADMIN_EMAIL = str()
QR_HOST = str()
HTTP_HOSTNAME = str()


def load_secret_keys():
    global APP_SECRET
    global DB_NAME
    global DB_SCHEMA
    global DB_HOST
    global DB_PORT
    global DB_USER
    global DB_PASSWORD
    global RECAPTCHA_SECRET
    global MANDRILL_API_KEY
    global MANDRILL_HOST
    global MANDRILL_PORT
    global MANDRILL_SMTP_USERNAME
    global MANDRILL_SMTP_PASSWORD
    global ADMIN_EMAIL
    global QR_HOST
    global HTTP_HOSTNAME

    def load_key(key):
        val = os.getenv(key)
        if val is not None:
            return str(val)
        else:
            raise ValueError('Missing secret_key "{}". Ask someone for it.'.format(key))

    APP_SECRET = load_key('APP_SECRET')
    DB_NAME = load_key('DB_NAME')
    DB_SCHEMA = load_key('DB_SCHEMA')
    DB_HOST = load_key('DB_HOST')
    DB_PORT = load_key('DB_PORT')
    DB_USER = load_key('DB_USER')
    DB_PASSWORD = load_key('DB_PASSWORD')
    RECAPTCHA_SECRET = load_key('RECAPTCHA_SECRET')
    MANDRILL_API_KEY = load_key('MANDRILL_API_KEY')
    MANDRILL_HOST = load_key('MANDRILL_HOST')
    MANDRILL_PORT = load_key('MANDRILL_PORT')
    MANDRILL_SMTP_USERNAME = load_key('MANDRILL_SMTP_USERNAME')
    MANDRILL_SMTP_PASSWORD = load_key('MANDRILL_SMTP_PASSWORD')
    ADMIN_EMAIL = load_key('ADMIN_EMAIL')
    QR_HOST = load_key('QR_HOST')
    HTTP_HOSTNAME = load_key('HTTP_HOSTNAME')

load_secret_keys()
