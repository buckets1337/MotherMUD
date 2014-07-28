#MUDserver.py tests

import mock
import sys, os
serverpath = os.path.abspath('../')
sys.path.insert(0, serverpath)
os.chdir('../')
import MUDserver
import clientInfo

class TestOnConnect():
	def mock_connection(self):
		self.connection = mock.Mock()
		self.connection.addrport = mock.Mock(return_value='192.168.1.1:1111')
		self.connection.send = mock.Mock(side_effect=self.set_message)
		return self.connection

	def set_message(self, message):
		self.connection.message = message

	def clear_global_data(self):
		MUDserver.CLIENT_DATA = {}
		MUDserver.CLIENT_LIST = []



	## Tests
	def test_onConnect_assign_to_CLIENT_DATA(self):
		self.clear_global_data()
		client = self.mock_connection()
		MUDserver.on_connect(client)
		assert '192.168.1.1:1111' in MUDserver.CLIENT_DATA
		
	def test_onConnect_message(self):
		self.clear_global_data()
		client = self.mock_connection()
		MUDserver.on_connect(client)
		assert self.connection.message == "\nWelcome to the MUD!\nPlease tell us your name.\n>>"

	def test_onConnect_client_info_creation(self):
		self.clear_global_data()
		client = self.mock_connection()
		MUDserver.on_connect(client)

		assert isinstance(MUDserver.CLIENT_DATA[client.addrport()], clientInfo.ClientInfo)

		assert MUDserver.CLIENT_DATA[client.addrport()].name == 'none'
		assert MUDserver.CLIENT_DATA[client.addrport()].prompt == '>>'
		assert MUDserver.CLIENT_DATA[client.addrport()].client == client
		assert len(MUDserver.CLIENT_LIST) == 1
		assert MUDserver.CLIENT_LIST[0] == client
		assert MUDserver.CLIENT_DATA[client.addrport()].clientDataID == str(client.addrport())

class TestOnDisconnect():
	def mock_connection(self):
		self.connection = mock.Mock()
		self.connection.addrport = mock.Mock(return_value='192.168.1.1:1111')
		self.connection.send = mock.Mock(side_effect=self.set_message)
		return self.connection

	def set_message(self, message):
		self.connection.message = message

