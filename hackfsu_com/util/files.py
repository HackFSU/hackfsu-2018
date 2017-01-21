"""
    Operations dealing with uploaded files
"""

from django.conf import settings
from api.models import Hackathon
import string
import random
import os

__all__ = []


UPLOAD_DIR = os.path.join(settings.BASE_DIR, './uploads')
MAX_FILE_NAME_SIZE = 60
MAX_NAME_SIZE = 30


def id_generator(size, chars=(string.ascii_uppercase + string.digits + string.ascii_lowercase)):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_file_name(original: str, file_extension: str) -> str:
    name = original[:MAX_NAME_SIZE]
    return name + '_' + id_generator(MAX_NAME_SIZE - len(name) - len(file_extension) - 2) + '.' + file_extension


def get_upload_relative_dir() -> str:
    """ Gets directory name based off of current hackathon """
    return '' + Hackathon.objects.current().id


def handle_file_upload(file, src_file_name: str, file_extension: str) -> str:
    """ Saves file and then returns the path to the file relative to the UPLOAD_DIR """
    while True:
        # Get file name that has not been taken
        relative_dir = get_upload_relative_dir()
        file_name = generate_file_name(src_file_name, file_extension)
        relative_path = os.path.join(relative_dir, './' + file_name)
        absolute_path = os.path.join(UPLOAD_DIR, './' + relative_path)
        if not os.path.isfile(absolute_path):
            break

    # Save file
    with open(absolute_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return relative_path
