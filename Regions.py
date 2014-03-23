# Regions.py
"""
contains all the regions in the game
"""
# Note: each region in the game should be added to 'list', and then have the region attributes defined.

import World



list = {}	# when adding regions to this list, do not ever assign values to the room list.  Rather, let Rooms.py handle assigning individual rooms to a region

list['test'] = World.Region(
	regionName = 'test',
	description = 'a testing region, will not be in the final game',
	)