#cPersonal.py
#
"""
Handles commands that alter character or client info
"""
def title(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	sets a client's title to whatever string they entered
	"""
	clientDataID = str(client.addrport())

	CLIENT_DATA[clientDataID].avatar.title = str(" ".join(args))
	client.send_cc("Title set to '%s'.\n" %CLIENT_DATA[clientDataID].avatar.title)