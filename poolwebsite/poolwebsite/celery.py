from __future__ import absolute_import
import os
from celery import Celery

#djcelery settings
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_TIMEZONE = 'UTC'

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poolwebsite.settings')

from django.conf import settings

app = Celery('poolwebsite')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

CELERYBEAT_SCHEDULE = {
    # Executes every minute
    'Check-Sensors': {
        'task': 'poolmonitor.tasks.read_sensors',
        'schedule': crontab(minute='*/1')
    },
}
