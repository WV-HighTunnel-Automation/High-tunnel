#!/usr/bin/python3

##Author:   Jeff Radabaugh
##Version:  1.0
##Date:     02-24-2017


#Import Section
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
config.read("/opt/TEMP-HUMIDITY/CONFIG/TempHumidity.config")

##      Defining Variables
if args.debug == "Y":
    email_list = config.get('EMAILS', 'debug_to_email_list').split(" ")
else:
    email_list = config.get('EMAILS', 'to_email_list').split(" ")
Type = config.get('THSENSOR', 'type')
Pin = config.get('THSENSOR', 'pin')
Max = float(config.get('THSENSOR', 'max'))
Min = float(config.get('THSENSOR', 'min'))
To = email_list
Subject = "High Tunnel Temperature and Humidity Reading"
temperature,humidity = GetTempHumidity(Type,Pin,)
USERNAME = config.get('EMAILS', 'username')
PASSWORD = config.get('EMAILS', 'password')
OutputFile = config.get('THSENSOR', 'output')

def CreateDataFile(temperature,humidity):
    target = open(OutputFile, 'a')
    Now = time.strftime("%d/%m/%Y %I:%M:%S")
    toutput = (" - The Temperature is {0:0.1f} inside the High Tunnel\n".format(temperature)) 
    houtput = (" - The Humidity is {0:0.1f}% inside the High Tunnel\n".format(humidity))
    target.write(Now)
    target.write(toutput)
    target.write(houtput)
    target.close

def Main():
    if args.debug == "Y":
        print("The Temperature is {0:0.1f} inside the High Tunnel\n".format(temperature))
        print("The Humidity is {0:0.1f}% inside the High Tunnel\n".format(humidity))
        Body = "The Temperature is {0:0.1f} inside the High Tunnel\n The Humidity is {1:0.1f}% inside the High Tunnel\n".format(temperature,humidity)
        #SendMail(To,Subject,Body)
    else:
        if temperature > Max:
            Body = "The Temperature is {0:0.1f} inside the High Tunnel raise the curtains\n The Humidity is {1:0.1f}% inside the High Tunnel\n".format(temperature,humidity)
        elif temperature < Min:
            #temperature = '{0:0.1f}'.format(temperature)
            Body = "The Temperature is {0:0.1f} inside the High Tunnel lower the curtains\n The Humidity is {1:0.1f}% inside the High Tunnel\n".format(temperature,humidity)
        else:
            Body = "The Temperature is {0:0.1f} inside the High Tunnel\n The Humidity is {1:0.1f}% inside the High Tunnel\n".format(temperature,humidity)
            print(Body)
            exit()
        #SendMail(To,Subject,Body)
    SendMail(To,Subject,Body,USERNAME,PASSWORD)
    CreateDataFile(temperature,humidity)

Main()
#SendMail(To,Subject,Body,USERNAME,PASSWORD)
#CreateDataFile(temperature,humidity)

