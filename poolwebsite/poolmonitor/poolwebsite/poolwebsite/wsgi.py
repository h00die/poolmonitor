"""
WSGI config for poolwebsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os,sys
sys.path.insert(0,os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poolwebsite.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
