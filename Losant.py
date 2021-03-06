from sys import *
from getopt import *
from os import *
import signal
import sys
import os
import types
import datetime
import re, time, csv
import OpenOPC
import time

import threading

from losantmqtt import Device

DEVICE_ID_GENERALE = '5dd6a3e00ac5cc0007fbfce8'
DEVICE_ID_GRUPPO_1 = '5dd7d0c2f0be720006b36741'
DEVICE_ID_GRUPPO_2 = '5dd7d122829bcb00065815e2'
DEVICE_ID_GRUPPO_3 = '5df25430aefa7f0008c2c9c6'

APP_KEY = 'e3262969-d61e-4a33-8c21-0a2b91408902'
APP_SECRET = 'b61138551a661bcfb851480cb9a70c319dcc8e4db073d8cb389523e314ddca91'


REGISTRO_DI_RESET_GENERALE = 'db200_dbx234_0'
REGISTRO_DI_RESET_GRUPPO_1 = 'db200_dbx234_1'
REGISTRO_DI_RESET_GRUPPO_2 = 'db200_dbx234_2'
REGISTRO_DI_RESET_GRUPPO_3 = 'db200_dbx234_3'


class Losant:
    ## Losant

    def __init__(self):
        try:
            self.deviceGenerale = Device(DEVICE_ID_GENERALE, APP_KEY, APP_SECRET)
            self.deviceGruppo1  = Device(DEVICE_ID_GRUPPO_1, APP_KEY, APP_SECRET)
            self.deviceGruppo2  = Device(DEVICE_ID_GRUPPO_2, APP_KEY, APP_SECRET)
            self.deviceGruppo3  = Device(DEVICE_ID_GRUPPO_3, APP_KEY, APP_SECRET)
        except:
            print('Error connecting losant')


    def connect(self):
        try:
            print('Connectiong to Losant...')
            self.deviceGenerale.connect(blocking=False)
            self.deviceGruppo1.connect(blocking=False)
            self.deviceGruppo2.connect(blocking=False)
            self.deviceGruppo3.connect(blocking=False)
            print('done')
        except:
            print('Error connecting losant')


    def sendData(self, data):
        try:
            losantDevice.send_state( data )

            # invio un boolean per tracciare se acceso o spento
            deviceGenerale.send_state( {"power_on" : True} )
            deviceGruppo1.send_state( data )
            deviceGruppo2.send_state( data )
            deviceGruppo3.send_state( data )
        except:
            print("Problem occurred sending data tot losant.")



    def notifyPlcIsOff(self):
        try:
            self.deviceGenerale.send_state( {"power_on" : False} )
        except:
            print("Problem occurred notifing off state to losant")



    def on_command(device, command):
        print(command["name"] + " command received.")

        # Listen for the gpioControl. This name configured in Losant
        if command["name"] == "reset_all":
            resetAll()
        elif command["name"] == "reset_gruppo_1":
            resetGruppo(1)
        elif command["name"] == "reset_gruppo_2":
            resetGruppo(2)
        elif command["name"] == "reset_gruppo_3":
            resetGruppo(3)


    def resetAll(self):
        self.global_var_1 = 'foo'


    def resetGruppo(self, numeroGruppo):
        if numeroGruppo == 1: reg = REGISTRO_DI_RESET_GRUPPO_1
        if numeroGruppo == 2: reg = REGISTRO_DI_RESET_GRUPPO_2
        if numeroGruppo == 3: reg = REGISTRO_DI_RESET_GRUPPO_3

        val = None

        try:
            val = opc.write( (reg, 1) )
            time.sleep(1.0)
        except OpenOPC.TimeoutError:
            print("TimeoutError occured.")

        return val
