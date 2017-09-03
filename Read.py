#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import binascii
import xmlrpclib
import sys
import time

host="http://192.168.0.24:9191/rpc/api/xmlrpc"
auth=""
proxy = xmlrpclib.ServerProxy(host)
continue_reading = True
userexist = False
debug_mode = True
cardid = ""
#statusOldCardId = False

def debug(message):
    if debug_mode:
        print message

# Read Card UID and check if user exist
def getUserName(card):
    username = proxy.api.lookUpUserNameByCardNo(auth, card)
    if len(username) >0:
        userexist = True
        debug(username)
        relayToggle(True)
    else:
        userexist = False
        relayToggle(False)
        debug("The card doesn't exist in the PaperCut system")

def relayToggle(status):
    GPIO.setup(22,GPIO.OUT)
    if status == True:
        debug("ON")
        #GPIO.output(22,True)
        #time.sleep(1)
    else:
        debug("OFF")
        #GPIO.output(22,False)
        #time.sleep(1)

def conToHex(UID):
    newUID = ""
    for i in xrange(0,4):
        newUID += format(UID[i],'02X')
    return newUID.upper()

def end_read(signal,frame):
    global continue_reading
    continue_reading = False
    GPIO.cleanup()


#----------------- MFRC522 ---------------------
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        cardid = conToHex(uid)
        if cardid == oldcardid:
            #statusOldCardId = True
            debug("OLD CARD")
        else:
            #statusOldCardId = False
            debug(cardid)
            getUserName(cardid)
    oldcardid = cardid
