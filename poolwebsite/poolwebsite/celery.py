from __future__ import absolute_import
import os, sys

#really unsure why i need to add this but uwsgi is failing miserably w/o it
sys.path.insert(0,'/webapps/venv/lib/python2.7/site-packages/')

from celery import Celery
# from celery.schedules import crontab

#djcelery settings
#CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
#CELERY_TIMEZONE = 'UTC'

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poolwebsite.settings')

from django.conf import settings

app = Celery('poolwebsite')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# CELERYBEAT_SCHEDULE = {
#     # Executes every minute
#     'Check-Sensors': {
#         'task': 'poolmonitor.tasks.read_sensors',
#         'schedule': crontab(minute='*/1')
#     },
# }

if __name__ == '__main__':
    app.start()
