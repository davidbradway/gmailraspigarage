#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""

"""
import sys
import os
import nmap                         # import nmap.py module
import time

WATCHEDMAC = "F4:F1:E1:41:12:02"

ISPI = 1
DEBUG = 0
USERNAME = "" # just the part before the @ sign, add yours here
PASSWORD = ""
GARAGE = 0 #Raspberry Pi GPIO Pin used for relay
MAIL_CHECK_FREQ = 10       # check mail interval wait [sec]

import feedparser, time
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
        # if the newest email was from me, then open garage
        if feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["entries"][-1]["author_detail"]["email"]  == USERNAME + '@gmail.com':
            print "start looking for phone before garage move"
            if ISPI:
                for x in range(0, 60):
                    print "Try %d" % (x)
                    found = 0
                    nm.scan(hosts='192.168.1.1-18', arguments='-sP -n')
                    for h in nm.all_hosts():
                         # Vendor list for MAC address
                         if 'mac' in nm[h]['addresses']:
                             #print(nm[h]['addresses']['mac'])
                            if nm[h]['addresses']['mac'] == WATCHEDMAC:
                                print "found MAC: " + nm[h]['addresses']['mac']
                                # open door
                                GPIO.output(GARAGE, False)
                                time.sleep(1)
                                GPIO.output(GARAGE, True)
                                found = 1
                                break
                    if found == 1:
                        break
                    else:
                        print "not found"
                        time.sleep(5)
    NEWMAIL_OFFSET = newmails
    time.sleep(MAIL_CHECK_FREQ)
