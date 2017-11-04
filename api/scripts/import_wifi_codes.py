"""
    Imports the wifi codes into the system. Does not import duplicates.

    Wifi code file format: lines of "<username> <password>"
"""

from django.conf import settings
from api.models import WifiCred, Hackathon
import os


INPUT_FILE_PATH = os.path.join(settings.BASE_DIR, './scripts/data/wifi-codes.txt')


def read_accounts() -> list:
    accounts = []
    with open(INPUT_FILE_PATH, 'r') as input_file:
        for line in input_file:
            words = line.split()
            accounts.append({
                'username': words[0].strip(),
                'password': words[1].strip()
            })
    return accounts


def remove_existing_accounts(accounts: list):
    h = Hackathon.objects.current()
    for account in list(accounts):
        if WifiCred.objects.filter(hackathon=h, username__iexact=account['username']).exists():
            accounts.remove(account)


def upload_accounts(accounts: list):
    h = Hackathon.objects.current()
    for account in accounts:
        WifiCred.objects.create(
            hackathon=h,
            username=account['username'],
            password=account['password']
        )


def run():
    accounts = read_accounts()
    print('Read in {} wifi accounts from file'.format(len(accounts)))
    remove_existing_accounts(accounts)
    print('Uploading {} new wifi accounts...'.format(len(accounts)), end='')
    upload_accounts(accounts)
    print('done.')
