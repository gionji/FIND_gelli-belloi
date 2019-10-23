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

import GelliBelloi

try:
	import Pyro
except ImportError:
	pyro_found = False
else:
	pyro_found = True

SERVER_NAME   = 'OPC.SimaticNET'
OPC_NAME_ROOT = 'S7:[Collegamento_IM151_8]'



GENERALE = 0
GRUPPO_1 = 1
GRUPPO_2 = 2
GRUPPO_3 = 3

FASI = 0
INGRESSI = 1
ALLARMI = 2

NOME = 0
INDIRIZZO = 1
TIPO = 2
NOTE = 3


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

# Chose the groups of vars
opcGroups = GelliBelloi.VAR_GROUPS_SUPER_COMPACT

# Initialize client DCOM mode
opc = OpenOPC.client()

# Get available servers on localhost
available_servers = opc.servers()

# Open Server
opc.connect( SERVER_NAME )

## read a GROUP of variable - opcGrops e' un array di stringhe
res = readGroupData(opcGroups)

labels = GelliBelloi.ALL_VARS_REORDERED

## qui e' come prendo le label ma vogli farlo a classi
print( GelliBelloi.Labels[GENERALE] )

print( GelliBelloi.Labels[GRUPPO_1][FASI] )
print( GelliBelloi.Labels[GRUPPO_1][INGRESSI] )
print( GelliBelloi.Labels[GRUPPO_1][ALLARMI] )

print( GelliBelloi.Labels[GRUPPO_2][FASI] )
print( GelliBelloi.Labels[GRUPPO_2][INGRESSI] )
print( GelliBelloi.Labels[GRUPPO_2][ALLARMI] )

print( GelliBelloi.Labels[GRUPPO_3][FASI] )
print( GelliBelloi.Labels[GRUPPO_3][INGRESSI] )
print( GelliBelloi.Labels[GRUPPO_3][ALLARMI] )

## stampo le dimensioni dei
if res != None:
    for var in res:
        print( len(value) )
