#!/usr/bin/python

import subprocess
import datetime
from ISStreamer.Streamer import Streamer
import sys
import os
import argparse
import re

INFO    = "\033[93m[-]\033[0m"
SUCCESS = "\033[92m[+]\033[0m"
FAIL    = "\033[91m[!]\033[0m"

#these initial values are overwritten if command line options are passed
apiKey = ""
sensors = ""
bucket = ""
units = "F"
base_dir    = '/sys/bus/w1/devices/'
device_file = '/w1_slave'

parser = argparse.ArgumentParser(description='A program to send (pool) temperature data from '+
                                 'a RaspberryPI to InitialState')
parser.add_argument("apiKey",  help="API Key for Initial State (www.initialstate.com)")
parser.add_argument("sensor",help="Sensor to probe, i.e. /sys/bus/w1/devices/SENSOR/w1_slave")
parser.add_argument("bucket",help="Bucket name on Initial State for this data")
parser.add_argument("-d", "--delay", default=900 ,type=int,
                    help="Delay between sensor reads (seconds)")
parser.add_argument("-c", "--celsius", action="store_true",
                    help="Use Celsius instead of Feirenheight")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

if not (apiKey or args.apiKey):
    print(FAIL, "APIKey Required")
    quit()
elif args.apiKey and not apiKey:
    apiKey = args.apiKey
    if args.verbose: print(SUCCESS, "APIKey set to: %s" %(apiKey))
if not re.match(r'[a-zA-Z0-9]{32}',apiKey):
    print(FAIL, "Invalid APIKey format.")
    quit()    

if not os.path.isfile('%s%s%s' %(base_dir, args.sensor, device_file)):
    print(FAIL, "Invalid Sensor: %s%s%s" %(base_dir, args.sensor, device_file))
    quit()

if args.celsius:
    units = "C"

#make sure the sensors are initialized
if verbose: print(SUCCESS, "Initializing w1 sensors")
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
#this lower portion of the code is loosely based off of Simon Monk's code @ https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software

def read_temp_raw(device):
    print(SUCCESS,'Reading Sensor %s' %(device))
    catdata = subprocess.Popen(['cat','%s%s%s' %(base_dir, device, device_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines

def save_result(sensor, lines, streamer):
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        if units == 'F':
            streamer.log(sensor, temp_f)
        elif units == 'C':
            streamer.log(sensor, temp_c)
        print(SUCCESS,'  Reading %s*%s' %(temp_f if units == 'F' else temp_c, units))
    else:
        print(FAIL,"Parse error in line: %s" %(lines))

#https://github.com/InitialState/python_appender/blob/master/example_app/example_command_line.py
def main():
    streamer = Streamer(bucket_name=bucket, access_key=access_key)

    try:
        while True:
            resultLines = read_temp_raw(args.sensor)
            save_result(args.sensor, resultLines, streamer)
    except KeyboardInterrupt:
        streamer.close()

if __name__ == "__main__":
	main()