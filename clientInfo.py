# clientInfo.py
"""
describes classes for holding info for the connected clients.
"""


class ClientInfo():
	"""
	Holds relevant data about a connected client.  Does not contain information about their avatar which is active in the world, but does contain a reference to it.
	"""
	def __init__(self, name, prompt, client, clientID, avatar=None):
		self.name = name
		self.prompt = prompt
		self.client = client
		self.clientID = clientID
		self.avatar = avatar