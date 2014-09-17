#!/usr/bin/env python

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

# my unread messages never goes to zero, yours might
NEWMAIL_OFFSET = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["feed"]["fullcount"])
while True:
    newmails = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["feed"]["fullcount"])
    if DEBUG:
        print newmails, "labeled mail commands!"
    
    if newmails > NEWMAIL_OFFSET: 
        # if the newest email was from me, then open garage
        if feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["entries"][-1]["author_detail"]["email"]  == USERNAME:
            print "garage move"
            if ISPI:
                GPIO.output(GARAGE, False)
                time.sleep(1)
                GPIO.output(GARAGE, True)
    NEWMAIL_OFFSET = newmails
    time.sleep(MAIL_CHECK_FREQ)
