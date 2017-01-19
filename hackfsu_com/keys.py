"""

Accessor for private keys in the environment

"""
import os
import json

APP_DEBUG = str(os.getenv('APP_DEBUG')).lower() == 'true'

APP_SECRET = os.getenv('APP_SECRET')
DB_NAME = os.getenv('DB_NAME')
DB_SCHEMA = os.getenv('DB_SCHEMA')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
RECAPTCHA_SECRET = os.getenv('RECAPTCHA_SECRET')
MANDRILL_API_KEY = os.getenv('MANDRILL_API_KEY')


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

    with open(os.path.dirname(os.path.abspath(__file__)) + '/secret_keys.json') as file:
        secret_keys = json.load(file)

        def set_if_exists(current, key):
            if key in secret_keys:
                return secret_keys[key]
            return current

        APP_SECRET = set_if_exists(APP_SECRET, 'APP_SECRET')
        DB_NAME = set_if_exists(DB_NAME, 'DB_NAME')
        DB_SCHEMA = set_if_exists(DB_SCHEMA, 'DB_SCHEMA')
        DB_HOST = set_if_exists(DB_HOST, 'DB_HOST')
        DB_PORT = set_if_exists(DB_PORT, 'DB_PORT')
        DB_USER = set_if_exists(DB_USER, 'DB_USER')
        DB_PASSWORD = set_if_exists(DB_PASSWORD, 'DB_PASSWORD')
        RECAPTCHA_SECRET = set_if_exists(RECAPTCHA_SECRET, 'RECAPTCHA_SECRET')
        MANDRILL_API_KEY = set_if_exists(MANDRILL_API_KEY, 'MANDRILL_API_KEY')


load_secret_keys()


