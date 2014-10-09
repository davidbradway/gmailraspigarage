#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
Script to check gmail for a new message with label 'Garage', when phone connects to wifi afterwards, open garage door
"""
import sys
import os
import nmap                # import nmap.py module dependency
import time
import feedparser

ISPI            = 1        # Is this being run on a Raspberry Pi?
DEBUG           = 0        # Should I print Debugging text output?
USERNAME        = "" # just the part before the @ sign, add yours here
PASSWORD        = ""
WATCHEDMAC      = ""
GARAGE          = 0        # Raspberry Pi GPIO Pin used for relay
MAIL_CHECK_FREQ = 10       # check mail interval wait [sec]
MOVE_YES        = 0        # Should I actually move the door?

if ISPI:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GARAGE, GPIO.OUT)

try:
    nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(1)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(1)

# my unread messages never goes to zero, yours might
NEWMAIL_OFFSET = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["feed"]["fullcount"])

while True:
    newmails = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["feed"]["fullcount"])
    if DEBUG:
        print newmails, "labeled mail commands!"
    
    if newmails > NEWMAIL_OFFSET: 
        # if the newest email was from me, then continue process to open garage
        if feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["entries"][-1]["author_detail"]["email"]  == USERNAME + '@gmail.com':
            print "Watch 5 minutes for phone to connect"
            for x in range(0, 60):
                print "Try %d" % (x+1)
                found = 0
                nm.scan(hosts='192.168.1.1-18', arguments='-sP -n')
                for h in nm.all_hosts():
                    if 'mac' in nm[h]['addresses']:
                        #print(nm[h]['addresses']['mac'])
                        if nm[h]['addresses']['mac'] == WATCHEDMAC:
                            print "found MAC: " + nm[h]['addresses']['mac']
                            # open door
                            if MOVE_YES:
                                print "moving door"
                                if ISPI:
                                    GPIO.output(GARAGE, False)
                                    time.sleep(1)
                                    GPIO.output(GARAGE, True)
                            found = 1
                            break
                if found:
                    break
                else:
                    print "not found"
                    time.sleep(5)
    NEWMAIL_OFFSET = newmails
    time.sleep(MAIL_CHECK_FREQ)

