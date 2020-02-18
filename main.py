from sys import *
from getopt import *
from os import *
import signal
import sys
import os
import types
import datetime
import re, time, csv
import time
import threading
from losantmqtt import Device
import requests
import json

import GelliBelloi
import StartIt
import OpcServer
import Losant

## Constants
DELAY = 0.1

## vars
isRunning = True
isPaused  = False

## losant methods

## startit methods


def handler_stop_signals(signum, frame):
    global isRunning
    isRunning = False


def main():
    ## manage the stop signals from O.S.
    # se faccio CTRL+C non blocca a caso
    signal.signal(signal.SIGINT, handler_stop_signals)
    signal.signal(signal.SIGTERM, handler_stop_signals)

    ## Connect to the opc server
    opcServer = OpcServer.OpcServer()
    opcServer.connect()

    ## Sonnect to losant
    losant = Losant.Losant()
    losant.connect()
    ## connect to Staartit ( anche se non serve)
    startIt = StartIt.StartIt()

    alarmsResetCounter = 0
    ALARMS_RESET_TH = 5

    while( isRunning ):
        ## get time
        now       = datetime.datetime.now()
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

        print('\n\n' + str(timestamp))

        ## Ask for the data to opc servers
        startItDataJson, losantDataJson = opcServer.getOpcDataInJsonFormats()

        if losantDataJson != None and startItDataJson != None:
            losant.sendData( losantDataJson )
            startIt.sendJson( startItDataJson )
        else:
            losant.notifyPlcIsOff()
            time.sleep(5)

        if alarmsResetCounter > ALARMS_RESET_TH:
            alarmsResetCounter = 0
            opcServer.resetAlarms()

        time.sleep( DELAY )



if __name__== "__main__":
    main()
