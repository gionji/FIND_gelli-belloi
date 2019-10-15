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
	
opc = OpenOPC.client()

opc.connect( SERVER_NAME )

for a in GelliBelloi.ALL_VARS_REORDERED:
    print(a)
