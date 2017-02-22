#!/usr/bin/python3

import sys
sys.path.append("/opt/PYTHON_LIBRARIES")
from Farm import *
import argparse


#Getting options from user
parser = argparse.ArgumentParser()
parser.add_argument('--to', action='store', default="", help="use --to to@gmail.com")
parser.add_argument('--from', action='store',default="Hightunnel", help="use --from who your email should be from")
parser.add_argument('--attach', action='store',default="", help="use --attach path to file to attach")
args = parser.parse_args()

Subject = "Temp Alert"
Body = "This is a Temperature problem in the High Tunnel"
['To'] = COMMASPACE.join(args.recipients)
['From'] = args.sender


# sendMail( ["mailto@gmail.com"],
#         "this is the subject",
#         "this is the body text of the email",
#         ["photo.jpg","text_file.txt"] )


SendMail( To,Subject,Body)