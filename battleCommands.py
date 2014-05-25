# battleCommands.py
# all player battle commands

def bash(client, args, CLIENT_LIST, CLIENT_DATA):
	'''
	whack the baddie with your weapon, or fists
	'''
	client.send("SMACK\n")