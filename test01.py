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


def readSingleData(variableName):
	val = None

	try:
		value, quality, time = opc.read( OPC_NAME_ROOT + 'variableName' )
	except OpenOPC.TimeoutError:
		print "TimeoutError occured"

	return val


def readGroupData(varGroup):
	val = None

	try:
		val = opc.read( varGroup )
	except OpenOPC.TimeoutError:
		print "TimeoutError occured"

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
valuesGrouped = readGroupData(varGroup)

## prova a leggere i singoli a parte
try:
	for var in valuesGrouped:
		print( len(value) )
except OpenOPC.TimeoutError:
	print "TimeoutError occured"
