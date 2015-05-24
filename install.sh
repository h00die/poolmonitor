#!/bin/bash
# does all the hard work to create/install everything required to run.

# Some of the links I used to help get this going.
# http://blog.mattwoodward.com/2013/01/setting-up-django-on-raspberry-pi.html
# http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html

sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get autoremove
sudo apt-get install python-dev python-setuptools python-pip nginx libpcre3 libpcre3-dev python-matplotlib liblapack-dev gfortran libblas-dev rabbitmq-server
sudo easy_install pip
sudo easy_install scipy
sudo pip install virtualenv virtualenvwrapper
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /etc/bash.bashrc
source /etc/bash.bashrc
sudo mkdir -p /webapps
sudo chown pi:pi /webapps
cd /webapps
git clone https://github.com/h00die/poolmonitor.git
mkvirtualenv /webapps/venv
cd /webapps/venv/bin/
source /webapps/venv/bin/activate
/webapps/venv/bin/pip install django==1.7.6 docutils pillow numpy scipy python-dateutil django-celery librabbitmq
cd /webapps
sudo ln -s /webapps/poolmonitor/poolwebsite/mysite_nginx.conf /etc/nginx/sites-enabled/
sudo rm  /etc/nginx/sites-enabled/default
python manage.py collectstatic --noinput
sudo mkdir -p /var/log/celery/run
sudo chmod -R 777 /var/log/celery
deactivate
sudo pip install uwsgi
sudo mkdir -p /etc/uwsgi/vassals
sudo ln -s /webapps/poolmonitor/poolwebsite/poolwebsite_uwsgi.ini /etc/uwsgi/vassals/
sudo touch /var/log/uwsgi.log
sudo chown www-data:www-data /var/log/uwsgi.log
sudo sed -i "/exit 0/c\printf \"Starting WSGI\"\n/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data\nexit 0" /etc/rc.local
#sudo sed -i "/import os/c\import os,sys\nsys.path.insert(0,\/webapps\/poolwebsite\/poolmonitor))" /webapps/poolwebsite/poolwebsite/wsgi.py
sudo su
echo "poolmonitor" > /etc/hostname
exit
source /webapps/venv/bin/activate
python /webapps/poolmonitor/poolwebsite/manage.py --noinput
deactivate
cp -r /usr/lib/pymodules/python2.7/matplotlib /webapps/venv/lib/python2.7
#sudo sed -i "/exit 0/c\printf \"Starting Celery\"\n/webapps/venv/bin/celery multi start w1 -A poolwebsite -B -l info --pidfile=/var/log/celery/run/%n.pid --logfile=/var/log/celery/%n%I.log\nexit 0" /etc/rc.local
sudo echo 'CELERYD_NODES="w1"
CELERY_BIN="/webapps/venv/bin/celery"

CELERY_APP="poolwebsite"
CELERYD_CHDIR="/webapps/poolmonitor/poolwebsite"
export DJANGO_SETTINGS_MODULE="poolwebsite.settings"

# Extra command-line arguments to the worker
#CELERYD_OPTS="--time-limit=300 --concurrency=8"

# %N will be replaced with the first part of the nodename.
CELERYD_LOG_FILE="/var/log/celery/%n.log"
CELERYD_PID_FILE="/var/log/celery/run/%n.pid"

# Workers should run as an unprivileged user.
#   You need to create this user manually (or you can choose
#   a user/group combination that already exists, e.g. nobody).
CELERYD_USER="www-data"
CELERYD_GROUP="www-data"

# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=1
' > /etc/default/celeryd

sudo echo 'CELERY_BIN="/webapps/venv/bin/celery"
CELERY_APP="poolwebsite"
CELERYBEAT_CHDIR="/webapps/poolmonitor/poolwebsite"
export DJANGO_SETTINGS_MODULE="poolwebsite.settings"

# Extra arguments to celerybeat
CELERYBEAT_OPTS="--schedule=/var/log/celery/celerybeat-schedule"
' > /etc/default/celerybeat

sudo wget "https://raw.githubusercontent.com/celery/celery/3.1/extra/generic-init.d/celerybeat" -O /etc/init.d/celerybeat
sudo wget "https://raw.githubusercontent.com/celery/celery/3.1/extra/generic-init.d/celeryd" -O /etc/init.d/celeryd
sudo chmod 755 /etc/init.d/celerybeat
sudo chmod 755 /etc/init.d/celeryd