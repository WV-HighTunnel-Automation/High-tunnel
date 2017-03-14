#!/usr/bin/python3

import psutil
import sys
import subprocess
sys.path.append("/opt/PYTHON_LIBRARIES")
from Farm import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--start", action="append",help="Use -d to run in debug mode") # Debug mode won`t email)
options, arguments = parser.parse_args()


def StartSoilMoisture():
	sm = subprocess.Popen([sys.executable, '/opt/SOIL-MOISTURE/moisture.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def StartTHMonitor():
	p = subprocess.Popen([sys.executable, '/opt/TEMP-HUMIDITY/TempHumMonitor.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def StartTHButton():
	p = subprocess.Popen([sys.executable, '/opt/TEMP-HUMIDITY/GetTHReading.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if not options.start:
	print("You must give a start option")

for proc in options.start:
	if proc == "SM":
		ProcRunning = ""
		ProcName = "moisture.py"
		ProcRunning=IsRunning(ProcName)
		if ProcRunning:
			print("%s is already running" % (ProcName))
		else:
			StartSoilMoisture()

	elif proc == "THB":
		ProcName = "GetTHReading.py"
		ProcRunning=IsRunning(ProcName)
		if ProcRunning:
			print("%s is already running" % (ProcName))
		else:
			StartTHButton()