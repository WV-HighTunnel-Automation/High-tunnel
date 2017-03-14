#!/usr/bin/python3

# Start by importing the libraries we want to use

import RPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import smtplib # This is the SMTP library we need to send the email notification
import time # This is the time library, we need this so we can use the sleep function
import sys
sys.path.append("/opt/PYTHON_LIBRARIES")
from Farm import *
import argparse
from configparser import ConfigParser


parser = argparse.ArgumentParser()
parser.add_argument('-d','--debug', action='store', default='',help='Use -d to run in debug mode') # Debug mode won`t email
args = parser.parse_args()


##      Setting up config parser
config = ConfigParser()
config.read("/opt/SOIL-MOISTURE/CONFIG/SoilMoisture.config")

# Define some variables to be used later on in our script

##      Defining Variables
if args.debug == "Y":
	email_list = config.get('EMAILS', 'debug_to_email_list').split(" ")
else:
	email_list = config.get('EMAILS', 'to_email_list').split(" ")
##Pin = config.get('SMSENSOR', 'pin')
To = email_list
Subject = "High Tunnel Sensor Alert"
USERNAME = config.get('EMAILS', 'username')
PASSWORD = config.get('EMAILS', 'password')
#OutputFile = config.get('SMSENSOR', 'output')
BodyDead = "Warning, no moisture detected! Plant death imminent!!!"
#Subject = "Moisture Sensor Notification"
BodyAlive = "Panic over! Plant has water again :)"
SensorList = config.get('SMSENSORS','sensors').split(" ")

# This is our callback function, this function will be called every time there is a change on the specified GPIO channel, in this example we are using 17

def callback(channel):  
	if GPIO.input(channel):
		print("%s LED off" % (channel))
		for sensor in SensorList:
			spin = int(config.get(sensor, 'pin'))
			if channel == spin:
				Subject = "%s Moisture Sensor Notification" % (sensor)
				SendMail(To,Subject,BodyDead,USERNAME,PASSWORD)

		#sendEmail(message_dead)
	else:
		print("%s LED on" % (channel))
		for sensor in SensorList:
			spin = int(config.get(sensor, 'pin'))
			if channel == spin:
				Subject = "%s Moisture Sensor Notification" % (sensor)
				SendMail(To,Subject,BodyAlive,USERNAME,PASSWORD)

		#sendEmail(message_alive)

def Main():
	for sensor in SensorList:
		pin = int(config.get(sensor, 'pin'))
		output = config.get(sensor, 'output')


		# Set our GPIO numbering to BCM
		GPIO.setmode(GPIO.BCM)

		# Define the GPIO pin that we have our digital output from our sensor connected to
		channel = pin
		# Set the GPIO pin to an input
		GPIO.setup(channel, GPIO.IN)

		# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
		GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
		# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
		GPIO.add_event_callback(channel, callback)

		# This is an infinte loop to keep our script running
	while True:
		# This line simply tells our script to wait 0.1 of a second, this is so the script doesnt hog all of the CPU
		time.sleep(0.1)

Main()
