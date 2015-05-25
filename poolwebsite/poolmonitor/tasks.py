from __future__ import absolute_import
import time
from poolmonitor import models
from django.utils import timezone
from celery import shared_task
import os

#this lower portion of the code is loosely based off of Simon Monk's code @ https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software

#this should be handled outside of this python script
#import os
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

def read_temp_raw(device):
    print('[+] Reading Sensor %s' %(device))
    base_dir    = '/sys/bus/w1/devices/'
    device_file = '/w1_slave'
    catdata = subprocess.Popen(['cat','%s%s%s' %(base_dir, device, device_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines

def save_result(sensor, lines):
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        if sensor.reading_units == 'F':
            r = models.Reading(reading = temp_f, reading_date = timezone.now, sensor = sensor)
            print('   Reading %s' %(temp_f))
        elif sensor.reading_units == 'C':
            r = models.Reading(reading = temp_c, reading_date = timezone.now, sensor = sensor)
            print('   Reading %s' %(temp_c))
        r.save()

@shared_task
def read_sensors():
    '''
        main loop for getting the sensors, and handling retrieving the data.
    '''
    for sensor in models.Sensor.objects.all():
        whenToPoll = sensor.reading.latest(reading_date)
        if whenToPoll:
            whenToPoll = whenToPoll + datetime.timedelta(0, 0, 0, 0, sensor.polling_interval) #minutes
            if whenToPoll <= timezone.now():
                lines = read_temp_raw(sensor.file_system_location)
                while lines[0].strip()[-3:] != 'YES':
                    time.sleep(0.2)
                    lines = read_temp_raw(sensor.file_system_location)
                    save_result(sensor, lines)
            else:
                print('[-] Sensor %s waiting on poll time of %s and its currently %s ' %(whenToPoll, tiemzone.now()))
                continue
        else:
            lines = read_temp_raw(sensor.file_system_location)
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw(sensor.file_system_location)
            save_result(sensor, lines)