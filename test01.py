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

import json

import GelliBelloi

try:
	import Pyro
except ImportError:
	pyro_found = False
else:
	pyro_found = True

SERVER_NAME   = 'OPC.SimaticNET'
OPC_NAME_ROOT = 'S7:[Collegamento_IM151_8]'


NOME = 0
INDIRIZZO = 1
TIPO = 2
NOTE = 3
LABEL = 4

LABEL = INDIRIZZO

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
    
    
    
    
def createJson(*elements):
    callerInfo = {
        "culture": "it-IT",
        "timezone": "+01:00",
        "version": "1.0.0" } 

    output = {}

    for couple in elements:
        if isinstance(couple,tuple) and len(couple) == 2 and len(couple[0]) == len(couple[1]):
            output.update( dict( zip( couple[0], couple[1] ) ) )
        else:
            print('Problem with data, impossible to create json')

    res = {'output' : output, 'callerInfo' : callerInfo}
    
    return json.dumps(res)


def sendJson():
    print("Sending json")
    print("DONE")
    

# Chose the groups of vars
opcGroups = GelliBelloi.VAR_GROUPS_SUPER_COMPACT

# Initialize client DCOM mode
opc = OpenOPC.client()

# Get available servers on localhost
available_servers = opc.servers()

# Open Server
opc.connect( SERVER_NAME )

## read a GROUP of variable - opcGrops e' un array di stringhe
res = readGroupData( opcGroups )


## stampo le dimensioni dei
if res != None:
    jjj = createJson( 
                (res[0], GelliBelloi.LabelsClass.Generale[ LABEL ] ),
                (res[1], GelliBelloi.LabelsClass.Gruppo1.Fasi[ LABEL ] ),
                (res[2], GelliBelloi.LabelsClass.Gruppo1.Ingressi[ LABEL ] ),
                (res[3], GelliBelloi.LabelsClass.Gruppo1.Allarmi[ LABEL ] ),
                (res[4], GelliBelloi.LabelsClass.Gruppo2.Fasi[ LABEL ] ),
                (res[5], GelliBelloi.LabelsClass.Gruppo2.Ingressi[ LABEL ] ),
                (res[6], GelliBelloi.LabelsClass.Gruppo2.Allarmi[ LABEL ] ),
                (res[7], GelliBelloi.LabelsClass.Gruppo3.Fasi[ LABEL ] ),
                (res[8], GelliBelloi.LabelsClass.Gruppo3.Ingressi[ LABEL ] ),
                (res[9], GelliBelloi.LabelsClass.Gruppo3.Allarmi[ LABEL ] )
                )

    print( jjj )

    sendJson()

else:
    print('cicciia! Nessun risultato, PLC spento')
