"""
Django settings for poolwebsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import absolute_import
import os,sys
sys.path.insert(0,'/webapps/poolwebsite/poolmonitor')
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import djcelery
from celery.schedules import crontab
djcelery.setup_loader()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'limx0r1a6526oe1dg9o)93r(v%6qmi_*38tiv*n8b4k0d1rwbn'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'poolmonitor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'poolwebsite.urls'

WSGI_APPLICATION = 'poolwebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'poolmonitor.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

#djcelery settings
CELERY_ACCEPT_CONTENT = ['json']
CELERYBEAT_SCHEDULE_FILENAME = "/var/log/celery/celerybeat_schedule"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks", )
CELERY_ALWAYS_EAGER = True
#BROKER_HOST = "localhost"
#BROKER_PORT = 5672
#BROKER_PASSWORD = "mypassword"
#BROKER_USER = "myuser"
#BROKER_VHOST = "localhost"
#BROKER_URL = "amqp://myuser:mypassword@localhost:5672//"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_TIMEZONE = TIME_ZONE
CELERYBEAT_SCHEDULE = {
    # Executes every minute
    'Check-Sensors': {
        'task': 'poolmonitor.tasks.read_sensors',
        'schedule': crontab(minute='*/1')
    },
}