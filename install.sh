#!/bin/bash
# does all the hard work to create/install everything required to run.

# Some of the links I used to help get this going.
# http://blog.mattwoodward.com/2013/01/setting-up-django-on-raspberry-pi.html
# http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html

sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get autoremove
sudo apt-get install python-dev python-setuptools python-pip ntp
sudo easy_install pip

# Initial State data streamer https://github.com/InitialState/python_appender
sudo pip install ISStreamer

sudo cp /usr/share/zoneinfo/America/New_York /etc/localtime
sudo echo "America/New_York" > /etc/timezone
sudo ntpd -q
