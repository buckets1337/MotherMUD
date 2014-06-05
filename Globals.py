# Globals.py
"""
This module is mostly just a placeholder for global data that is shared between module.
Separating this data out encourages better encapsulation, and allows modules that are being
imported into MUDserver.py to still reference these values
"""

# IDLE_TIMEOUT = 300
# CLIENT_LIST = []
# SERVER_RUN = True
# CLIENT_DATA = {}
# TIMERS = []






IDLE_TIMEOUT = 300
CLIENT_LIST = []
SERVER_RUN = True
CLIENT_DATA = {}
TIMERS = []
MoveTIMERS = []

OPList = []

RegionsList = ['test', 'testb', 'Onette']
masterRooms = {}
regionListDict = {}
battleRooms = []
#initializeMasterRooms(RegionsList)
fromFileList = []
mobsFromFile = []
startingRoom = None

