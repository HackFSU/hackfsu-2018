"""
    Operations dealing with uploaded files
"""

from django.conf import settings
import string
import random
import os
import logging

MAX_FILE_NAME_SIZE = 60
MAX_NAME_SIZE = 30


def id_generator(size, chars=(string.ascii_uppercase + string.digits + string.ascii_lowercase)):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_file_name(original: str, file_extension: str) -> str:
    name = original[:MAX_NAME_SIZE]
    return name + '_' + id_generator(MAX_FILE_NAME_SIZE - len(name) - len(file_extension) - 1) + file_extension


def get_absolute_path(relative_file_path):
    return os.path.normpath(os.path.join(settings.MEDIA_ROOT, './' + relative_file_path))


def size_in_mb(absolute_file_path) -> float:
    return os.path.getsize(absolute_file_path) / (2**20 * 1.0)


def handle_file_upload(file, media_directory_path: str, src_file_name: str, file_extension: str) -> str:
    """ Saves file and then returns the path to the file relative to the UPLOAD_DIR """
    while True:
        # Get file name that has not been taken
        file_name = generate_file_name(src_file_name, file_extension)
        relative_path = os.path.normpath(os.path.join(media_directory_path, './' + file_name))
        absolute_path = get_absolute_path(relative_path)
        if not os.path.isfile(absolute_path):
            break

    # Ensure directory exists
    os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

    # Save file
    with open(absolute_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    logging.info('Uploaded new {}mb file "{}"'.format(size_in_mb(absolute_path), relative_path))
    return relative_path


def get_url(relative_file_path):
    """ Gets the url path to given relative_file_path, which has already been made """
    return os.path.normpath((os.path.join(settings.MEDIA_URL, './' + relative_file_path)))


def delete_if_exists(relative_file_path):
    abs_path = get_absolute_path(relative_file_path)
    if os.path.exists(abs_path):
        os.remove(abs_path)
        logging.info('Deleted uploaded file "{}"'.format(abs_path))
    else:
        logging.warning('Attempted to delete non-existing uploaded file "{}"'.format(abs_path))
