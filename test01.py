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

LABELS = 1
DATA = 0

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
            
        if not isinstance(couple,tuple):
            print('Problem with data: nON E UNATUPLA')
        elif not len(couple) == 2:
            print('Problem with data: non ci sono due elementi nella tupla: ', len(couple))
        elif not len(couple[LABELS]) == len(couple[DATA]):
            print('Problem with data: le liste non sono lunghe uguali: ', len(couple[DATA]), len(couple[LABELS]))
            for i in range(0, max(len(couple[DATA]), len(couple[LABELS])) - 1):
                print(i, couple[DATA][i], couple[LABELS][i])
        else:
            print( 'OK' )
            output.update( dict( zip( couple[LABELS], couple[DATA] ) ) )

    res = {'output' : output, 'callerInfo' : callerInfo}
    
    return res


def sendJson(msg):
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
#print(res)

##per prendere un colonna sola
#print( [elem[ LABELS ] for elem in GelliBelloi.Labels.Gruppo2.Fasi] )


## stampo le dimensioni dei
while True:
    
    res = readGroupData( opcGroups )
    
    if res != None:
        jjj = createJson( 
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
        print('Data readed!')
        #print(json.dumps(jjj, indent=2, sort_keys=True))

        sendJson(jjj)

    else:
        print('cicciia! Nessun risultato, PLC spento')
