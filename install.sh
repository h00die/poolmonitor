#!/bin/bash
# does all the hard work to create/install everything required to run.

# Some of the links I used to help get this going.
# http://blog.mattwoodward.com/2013/01/setting-up-django-on-raspberry-pi.html
# http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html

sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get autoremove
sudo apt-get install python-dev python-setuptools python-pip nginx libpcre3 libpcre3-dev python-matplotlib liblapack-dev gfortran libblas-dev ntp
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
/webapps/venv/bin/pip install django==1.7.6 docutils pillow numpy scipy python-dateutil
cd /webapps
sudo ln -s /webapps/poolmonitor/poolwebsite/mysite_nginx.conf /etc/nginx/sites-enabled/
sudo rm  /etc/nginx/sites-enabled/default
python manage.py collectstatic --noinput
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
python /webapps/poolmonitor/poolwebsite/manage.py makemigrations --noinput
python /webapps/poolmonitor/poolwebsite/manage.py syncdb --noinput
sudo chown -R www-data /webapps/poolmonitor/

deactivate
cp -r /usr/lib/pymodules/python2.7/matplotlib /webapps/venv/lib/python2.7

sudo echo "America/New_York" > /etc/timezone
sudo update-rc.d -f ntp remove
sudo update-rc.d ntp defaults
sudo ntpd -q
sudo sed -i "/exit 0/c\printf \"Updating Time\"\nntpd -q\nexit 0" /etc/rc.local

line="* * * * * /webapps/venv/bin/python /webapps/poolmonitor/poolwebsite/manage.py get_sensor_data"
(crontab -l; echo "$line" ) | crontab -