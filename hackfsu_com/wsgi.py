"""
WSGI config for hackfsu_com project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackfsu_com.settings')
os.environ.setdefault('PATH_PROJECT', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('PATH_ENVIRONMENT_PACKAGES', os.path.join(
    os.environ.get('PATH_PROJECT'), './venv/lib/python3.5/site-packages'))

sys.path.append(os.environ.get('PATH_PROJECT'))
sys.path.append(os.environ.get('PATH_ENVIRONMENT_PACKAGES'))

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
