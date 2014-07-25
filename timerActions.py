#timerActions.py
#various functions intended to run at the end of Timers



def kick(client, timer, timerList):
	'''
	disconnects <client>
	'''
	client.active = False
	timerList.remove(timer)
