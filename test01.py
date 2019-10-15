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
available_servers = OpenOPC.servers()

# Open Server
opc.connect( SERVER_NAME )

## To read data ...
value, quality, time = opc.read( OPC_NAME_ROOT + 'Status.Generale' )

## Short version ... onliy data
#value = opc['Random.Int4']

#opc.read( opcGroups )



