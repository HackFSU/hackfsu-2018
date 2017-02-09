"""
    Exports all user names and emails to a CSV
"""

from django.contrib.auth.models import User
from django.conf import settings
import os
import csv


OUTPUT_PATH = os.path.join(settings.BASE_DIR, './scripts/data/exported_users.csv')


def run():
    users = User.objects.all().order_by('email')

    with open(OUTPUT_PATH, 'w') as csv_file:
        data_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        data_writer.writerow(['Email', 'First Name', 'Last Name'])

        for user in users:
            data_writer.writerow([user.email, user.first_name, user.last_name])

