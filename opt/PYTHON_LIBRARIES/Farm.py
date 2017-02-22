#!/usr/bin/python3

##Author:   Jeff Radabaugh
##Version:  1.0
##Date:     02-24-2017

#Import Section
import time
import os
import sys
from shutil import copyfile
from pathlib import Path
from configparser import ConfigParser
import smtplib
import email
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import Adafruit_DHT

#Variable Declaration
#THconfig = ConfigParser()
#THconfig.read("/opt/TEMP-HUMIDITY/CONFIG/TempHumidity.config")



def GetTempHumidity(Type,Pin,):
	sensor = Type
	pin = Pin
	
	if sensor == "2302":
		sensor = Adafruit_DHT.AM2302

	# Try to grab a sensor reading.  Use the read_retry method which will retry up
	# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	# Un-comment the line below to convert the temperature to Fahrenheit.
	temperature = temperature * 9/5.0 + 32
	# Note that sometimes you won't get a reading and
	# the results will be null (because Linux can't
	# guarantee the timing of calls to read the sensor).
	# If this happens try again!
	if humidity is not None and temperature is not None:
		return(temperature,humidity)
	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)

def SendMail(ToAddress,Subject,Body,USERNAME,PASSWORD):
	MAILTO  = ToAddress
	MAILFROM = "High Tunnel"
	msg = MIMEText(Body)
	msg['Subject'] = Subject
	msg['From'] = MAILFROM
	msg['To'] = ", ".join(MAILTO)

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo_or_helo_if_needed()
	server.starttls()
	server.ehlo_or_helo_if_needed()
	server.login(USERNAME,PASSWORD)
	server.sendmail(USERNAME, MAILTO, msg.as_string())
	server.quit()

def SendMailAttachment(ToAddress,FromAddress,Subject,text,USERNAME,PASSWORD,files=[]):
	MAILTO  = ToAddress
	MAILFROM = FromAddress
	assert type(files)==list
	msg = MIMEMultipart()
	msg['From'] = USERNAME
	msg['To'] = ", ".join(MAILTO)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = Subject
	msg.attach( MIMEText(text) )

	for f in files or []:
		with open(f, "rb") as fil:
			part = MIMEApplication(fil.read(),Name=basename(f))
			part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
			msg.attach(part)


	# for file in files:
	# 	part = MIMEBase('application', "octet-stream")
	# 	part.set_payload( open(file,"rb").read() )
	# 	Encoders.encode_base64(part)
	# 	part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
	# 	msg.attach(part)

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo_or_helo_if_needed()
	server.starttls()
	server.ehlo_or_helo_if_needed()
	server.login(USERNAME,PASSWORD)
	server.sendmail(USERNAME, MAILTO, msg.as_string())
	server.quit()





	



