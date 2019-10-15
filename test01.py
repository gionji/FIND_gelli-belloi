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


opcGroups = GelliBelloi.VAR_GROUPS_SUPER_COMPACT
	
# Initialize client DCOM mode	
opc = OpenOPC.client()

# Get available servers on localhost
available_servers = opc.servers()

# Open Server
opc.connect( SERVER_NAME )

## To read data ...
try:
	value, quality, time = opc.read( OPC_NAME_ROOT + 'Status.Generale' )
except OpenOPC.TimeoutError:
	print "TimeoutError occured"

## Short version ... onliy data
#value = opc['Random.Int4']

## read a grop of variable - opcGrops e' un array di stringhe
#opc.read( opcGroups )

## prova a leggere i singoli a parte
for var in opcGroups:
	print( var )
	value = opc[ var ]
	print( value )

