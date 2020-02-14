#!C:\Python27\python.exe

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

import requests
import json
import GelliBelloi


try:
	import Pyro
except ImportError:
	pyro_found = False
else:
	pyro_found = True


WEB_SERVICE = 'https://f2tapiv2-staging.azurewebsites.net/api/PLC/send'
WEB_SERVICE = 'https://servicesv2.fleet2track.com//api/PLC/send'

MACHINERY_ID = 'gelli-belloi_01'

SERVER_NAME   = 'OPC.SimaticNET'
OPC_NAME_ROOT = 'S7:[Collegamento_IM151_8]'


NOME = 0
INDIRIZZO = 1
TIPO = 2
NOTE = 3
LABEL = 4

LABEL = INDIRIZZO

LABELS = 1
DATA = 0

DELAY = 1.0 # seconds

## Losant
DEVICE_ID          = '5dca7e9585f56300066d2e45'
DEVICE_ID_GENERALE = '5dd6a3e00ac5cc0007fbfce8'

DEVICE_ID_GRUPPO_1 = '5dd7d0c2f0be720006b36741'
DEVICE_ID_GRUPPO_2 = '5dd7d122829bcb00065815e2'
DEVICE_ID_GRUPPO_3 = '5df25430aefa7f0008c2c9c6'

# APP_KEY = '5a406d76-2b01-4074-a5d2-5d7bb70a8544'
APP_KEY = 'e3262969-d61e-4a33-8c21-0a2b91408902'

# APP_SECRET = '20831052b9ab7e395bac4d2b54c2f4ba053ab5f80a2850ea97ca732285e8b9df'
APP_SECRET = 'b61138551a661bcfb851480cb9a70c319dcc8e4db073d8cb389523e314ddca91'


losantDevice   = None
deviceGenerale = None
deviceGruppo1  = None
deviceGruppo2  = None
deviceGruppo3  = None

REGISTRO_DI_RESET_GENERALE = 'S7:[Collegamento_IM151_8]ResetAllarmi'
REGISTRO_DI_RESET_GRUPPO_1 = 'db200_dbx234_1'
REGISTRO_DI_RESET_GRUPPO_2 = 'db200_dbx234_2'
REGISTRO_DI_RESET_GRUPPO_3 = 'db200_dbx234_3'


ALARM_RESET_TH = 5


def readSingleData(variableName):
	val = None

	try:
		value, quality, time = opc.read( OPC_NAME_ROOT + 'variableName' )
	except OpenOPC.TimeoutError:
		print "TimeoutError occured: IL PLC E SPENTO!!!"

	return val


def readGroupData(varGroup):
	val = None

	try:
		val = opc.read( varGroup )
	except OpenOPC.TimeoutError:
		print "TimeoutError occured: IL PLC E SPENTO!!!"

	return val



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


def resetGruppo(self, numeroGruppo):
    if numeroGruppo == 1: reg = REGISTRO_DI_RESET_GRUPPO_1
    if numeroGruppo == 2: reg = REGISTRO_DI_RESET_GRUPPO_2
    if numeroGruppo == 3: reg = REGISTRO_DI_RESET_GRUPPO_3

    val = None

    try:
        val = opc.write( (reg, 1) )
        time.sleep(1.0)
        val = opc.write( (reg, 0) )
    except OpenOPC.TimeoutError:
        print "TimeoutError occured."

    return val


def resetAll():
    val = None

    try:
        val = opc.write( (REGISTRO_DI_RESET_GENERALE, 1) )
    except OpenOPC.TimeoutError:
        print "TimeoutError occured: IL PLC E SPENTO!!!"

    return val



def createJson(*elements):
    callerInfo = {
        "culture": "it-IT",
        "timezone": "+01:00",
        "version": "1.0.0" }

#    output = {"machineryId": "gelli-belloi_01", "timestamp":"dd/MM/yyyy HH:mm:ss"}
    output = { "machineryId" : MACHINERY_ID }

    try:
        for couple in elements:

            if not isinstance(couple,tuple):
                print('Problem with data: nON E UNATUPLA')
            elif not len(couple) == 2:
                print('Problem with data: non ci sono due elementi nella tupla: ', len(couple))
            elif not len(couple[LABELS]) == len(couple[DATA]):
                print('Problem with data: le liste non sono lunghe uguali: ', len(couple[DATA]), len(couple[LABELS]))
                for i in range(0, max(len(couple[DATA]), len(couple[LABELS])) - 1):
                    print(i, couple[DATA][i], couple[LABELS][i])
            else:
                # print( 'OK' )
                output.update( dict( zip( couple[LABELS], couple[DATA] ) ) )
    except Exception as e:
        print( str(e) )
        return None
        
    startitJson = {'output' : output, 'callerInfo' : callerInfo}

    return startitJson, output


def sendJson(msg):
    url = WEB_SERVICE
    data = msg
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        #print('HTTP error occurred: ', http_err)  # Python 3.6
        return ('Send json - HTTP error occurred: ', http_err)  # Python 3.6
    except Exception as err:
        #print('Other error occurred:', err)  # Python 3.6
        return ('Send json - Other error occurred:', err)
    else:
        #print('Success!')
        return 'Send json: success' 



def sendToLosant( jsonData):
    print("Sending Device State")
    losantDevice.send_state( jsonData )


# Chose the groups of vars
opcGroups = GelliBelloi.VAR_GROUPS_SUPER_COMPACT

# Initialize client DCOM mode
opc = OpenOPC.client()

# Get available servers on localhost
available_servers = opc.servers()

# Open Server
opc.connect( SERVER_NAME )

## read a GROUP of variable - opcGrops e' un array di stringhe
#res = readGroupData( opcGroups )


## connect to losant
# Construct Losant device
try:
    print('Connectiong to Losant...')
    losantDevice   = Device(DEVICE_ID,          APP_KEY, APP_SECRET)
    deviceGenerale = Device(DEVICE_ID_GENERALE, APP_KEY, APP_SECRET)
    deviceGruppo1  = Device(DEVICE_ID_GRUPPO_1, APP_KEY, APP_SECRET)
    deviceGruppo2  = Device(DEVICE_ID_GRUPPO_2, APP_KEY, APP_SECRET)
    deviceGruppo3  = Device(DEVICE_ID_GRUPPO_3, APP_KEY, APP_SECRET)
    
    losantDevice.connect(blocking=False)
    deviceGenerale.connect(blocking=False)
    deviceGruppo1.connect(blocking=False)
    deviceGruppo2.connect(blocking=False)
    deviceGruppo3.connect(blocking=False)
    
    # Listen for commands.
    deviceGenerale.add_event_observer("command", on_command)
    print('done')
except:
    print('Error connecting losant')

ALARM_RESET_TH = 10
resetAlarmsCounter = 0

## stampo le dimensioni dei
while( True ):
	## read a GROUP of variable - opcGrops e' un array di stringhe
    res = None
    print('Reading data from opc...')
    res = readGroupData( opcGroups )
    print('done')
    
    ## print content from opc
    #print('Opc call result:',res)
  
    resetAlarmsCounter = resetAlarmsCounter + 1
  
    ## get time
    now = datetime.datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    
    if res != None:
        try:
            dataStartit, dataLosant = createJson(
                        (res[0][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Generale] ),
                        (res[1][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo1.Fasi] ),
                        (res[2][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo1.Ingressi] ),
                        (res[3][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo1.Allarmi] ),
                        (res[4][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo2.Fasi] ),
                        (res[5][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo2.Ingressi] ),
                        (res[6][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo2.Allarmi] ),
                        (res[7][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo3.Fasi] ),
                        (res[8][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo3.Ingressi] ),
                        (res[9][1], [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo3.Allarmi] )
                        ) 
            ## Print created json with nice indentation
            #print(json.dumps(jjj, indent=4, sort_keys=True))

            ## send data to startIt
            print('Sending data to Startit...')
            responseFromStartit = sendJson( dataStartit )
            print(responseFromStartit)
            
            ## send data to losant
            print('Sending data to Losant...')
            responseFromLoasant = losantDevice.send_state( dataLosant )
            
            # invio un boolean per tracciare se acceso o spento
            deviceGenerale.send_state( {"power_on" : True} )
            deviceGruppo1.send_state( dataLosant )
            deviceGruppo2.send_state( dataLosant )
            deviceGruppo3.send_state( dataLosant )
            print('done')
            
        except Exception as e:
            print(str(timestamp), str(e))
        
    else:
        # in caso di PLC SPENTO
        print(str(timestamp), 'PLC spento')
        deviceGenerale.send_state( {"power_on" : False} )
        ## ritardo in caso di PLC spento
        time.sleep( DELAY )
        
    if resetAlarmsCounter == ALARM_RESET_TH:
        resetAll()
        resetAlarmsCounter = 0
        print("Reset all alarms.")        

    time.sleep( DELAY )
    print("")
