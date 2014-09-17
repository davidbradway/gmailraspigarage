#!/usr/bin/env python

#see http://blog.scphillips.com/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

import RPi.GPIO as GPIO, feedparser, time

DEBUG = 1
USERNAME = "" # just the part before the @ sign, add yours here
PASSWORD = ""
MAIL_CHECK_FREQ = 10       # check mail interval wait [sec]
GPIO.setmode(GPIO.BCM)
GARAGE = 0
GPIO.setup(GARAGE, GPIO.OUT)

                           # my unread messages never goes to zero, yours might
NEWMAIL_OFFSET = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["feed"]["fullcount"])

while True:
    newmails = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["feed"]["fullcount"])

    if DEBUG:
        print "There were", newmails, "commands received!"

    if newmails > NEWMAIL_OFFSET:
        print "garage move" 
        GPIO.output(GARAGE, False)
        time.sleep(1)
        GPIO.output(GARAGE, True)
        NEWMAIL_OFFSET = newmails
    else:
        NEWMAIL_OFFSET = newmails

    time.sleep(MAIL_CHECK_FREQ)
