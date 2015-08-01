#!/bin/bash
# does all the hard work to create/install everything required to run.

sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get autoremove
sudo apt-get install python-pip

# Initial State data streamer https://github.com/InitialState/python_appender
sudo pip install ISStreamer

echo "dtoverlay=w1-gpio" >> /boot/config.txt