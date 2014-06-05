# aiMove.py
# various movement AI scripts for mobs

import random
import Globals





class Timer:		# this was copied directly from World.py, and should be exactly the same at all times.
    """
    A timer is an object that, when spawned, will count down until zero, and then perform and action and possibly respawn itself
    """
    def __init__(self, TIMERS, time, actionFunction, actionArgs = [], attachedTo = None, respawns = False):
        self.TIMERS = TIMERS
        self.time = time
        self.actionFunction = actionFunction
        self.actionArgs = actionArgs
        self.attachedTo = attachedTo
        self.respawns = respawns

        self.currentTime = float(time)

        self.count = 0

        self.TIMERS.append(self)

        # self.initialTime = time.clock()
        # self.lastTime = 0

    def tick(self, deltaTime):     
        """tick should be called once each game loop"""
        #timePassed = (time.clock() - self.initialTime) - self.lastTime

        self.currentTime -= deltaTime
        #print self.currentTime
        #print "tick"
        self.count += 1
        #print str(self.count) + self.attachedTo.owner.owner.name

        if self.currentTime <= 0:

			#print "time out. " + str(self.attachedTo.owner.owner.name) + " " + str(self)
			if self in Globals.TIMERS:
				Globals.TIMERS.remove(self)
			elif self in Globals.MoveTIMERS:
				Globals.MoveTIMERS.remove(self)

			#print "removed " + str(self)

			if self.actionArgs != []:
				self.actionFunction(self.actionArgs)
			else:
			    self.actionFunction()


			#print "timers:" + str(Globals.TIMERS)


			# if self.respawns == True:
			#     self.currentTime = self.time
			#     Globals.TIMERS.append(self)
#---------------------------------------------------------

class movementAI:
	def __init__(self, mob, time):
		self.mob = mob
		self.time = time
		self.Timer = Timer(Globals.MoveTIMERS, self.time, None, None, self, True)
		

	def selector(self, oddsList):     # pick a random selection from an odds list and return it.
                            # an odds list is a list containing any number of smaller lists, each with the format of [<choice>,<odds value>]
	    totalOdds = 0

	    for sel in oddsList:
	        totalOdds += sel[1]

	    oddSum = 0
	    selection = random.randint(0, totalOdds)
	    for sel in oddsList:
	        oddSum += sel[1]
	        if oddSum >= selection:
	            break
	    # print sel
	    return sel

	def introvertRandom(self, args):		# randomly chooses an exit, and takes it.  Much greater chances of moving when mobs of the same type are in the room.
		odds = 1					# Essentially, these mobs flee other mobs of their own type.  They want to find their own room.
		for mob in self.mob.currentRoom.mobs:
			odds +=1
		#check if mob should move
		oddsList = [[True, odds], [False, 2]]	#basic 50/50 odds to move with one other mob present, with the odds increasing as the number of mobs in the room goes up
		winner = self.selector(oddsList)
		#if mob should move, select a random exit and move there
		# if self.mob.currentRoom != None:
		# 	print "  moveCheck - " + str(self.mob.name) +"["+ str(self.mob.currentRoom.region) + ":" + str(self.mob.currentRoom.name) +"]" + " " + str(winner)
		# else:
		# 	print "  moveCheck - " + str(self.mob.name) + " " + str(winner)
		if winner[0] == 'True' or winner[0] == True:
			newRoom = None
			if self.mob.currentRoom != None:
				randRange = len(self.mob.currentRoom.exits) - 1
				selection = random.randint(0, randRange)
				exitList = []
				for exit in self.mob.currentRoom.exits:
					exitList.append(exit)
				# print exitList

				selectedExit = exitList[selection]
				if self.mob.currentRoom.name == selectedExit:
					selectedExit = None

				for room in Globals.regionListDict[self.mob.currentRoom.region]:
					if Globals.regionListDict[self.mob.currentRoom.region][room].name == selectedExit:
						newRoom = Globals.regionListDict[self.mob.currentRoom.region][room]

				if newRoom != None:
					for player in self.mob.currentRoom.players:
						player.client.send_cc("^y%s left.^~\n" %self.mob.name.capitalize())

					oldMobRoom = self.mob.currentRoom

					self.mob.currentRoom.mobs.remove(self.mob)
					self.mob.currentRoom = newRoom
					newRoom.mobs.append(self.mob)

					print "Mm " + str(self.mob) + " " + str(self.mob.name) + ": from [" + str(oldMobRoom.region) +":"+ str(oldMobRoom.name) + "] to [" + str(self.mob.currentRoom.region) +":"+ str(self.mob.currentRoom.name) + "]"

					for player in self.mob.currentRoom.players:
						player.client.send_cc("^yA %s has entered.^~\n" %self.mob.name)

		self.resetTimer()

	def extrovertRandom(self, args):		# randomly chooses an exit, and takes it.  Much greater chances of moving when there are no other mobs of the same type in the room.
		odds = 0					# this AI tends to cause mobs to 'clump up' in a room, with them being less prone to leaving a room the more mobs of the same type that arrive.
		for mob in self.mob.currentRoom.mobs:
			if mob.name == self.mob.name:
				odds +=1
		#check if mob should move
		oddsList = [[True, 2], [False, odds]]	#basic 50/50 odds to move when one other mob is present, with the odds decreasing as the number of mobs in the room of the same type goes up
		winner = self.selector(oddsList)
		#if mob should move, select a random exit and move there
		# if self.mob.currentRoom != None:
		# 	print "  moveCheck - " + str(self.mob.name) +"["+ str(self.mob.currentRoom.region) + ":" + str(self.mob.currentRoom.name) +"]" + " " + str(winner)
		# else:
		# 	print "  moveCheck - " + str(self.mob.name) + " " + str(winner)
		if winner[0] == 'True' or winner[0] == True:
			newRoom = None
			if self.mob.currentRoom != None:
				randRange = len(self.mob.currentRoom.exits) - 1
				selection = random.randint(0, randRange)
				exitList = []
				for exit in self.mob.currentRoom.exits:
					exitList.append(exit)
				# print exitList

				selectedExit = exitList[selection]
				if self.mob.currentRoom.name == selectedExit:
					selectedExit = None

				for room in Globals.regionListDict[self.mob.currentRoom.region]:
					if Globals.regionListDict[self.mob.currentRoom.region][room].name == selectedExit:
						newRoom = Globals.regionListDict[self.mob.currentRoom.region][room]

				if newRoom != None:
					for player in self.mob.currentRoom.players:
						player.client.send_cc("^y%s left.^~\n" %self.mob.name.capitalize())

					oldMobRoom = self.mob.currentRoom

					if self.mob in self.mob.currentRoom.mobs:
						self.mob.currentRoom.mobs.remove(self.mob)
						self.mob.currentRoom = newRoom
						newRoom.mobs.append(self.mob)

					print "Mm " + str(self.mob) + " " + str(self.mob.name) + ": from [" + str(oldMobRoom.region) +":"+ str(oldMobRoom.name) + "] to [" + str(self.mob.currentRoom.region) +":"+ str(self.mob.currentRoom.name) + "]"

					for player in self.mob.currentRoom.players:
						player.client.send_cc("^yA %s has entered.^~\n" %self.mob.name)

				else:
					if self.Timer in Globals.MoveTIMERS:
						Globals.MoveTIMERS.remove(self.Timer)

				

		self.resetTimer()


	def doNotMove(self, args):		# don't ever move from the room the mob spawned in
		self.resetTimer()


	def basicRandom(self, args):	# randomly choose an exit, and take it.  Unaffected by number of mobs in the room, always 50/50 chance of moving
		oddsList = [[True, 4], [False, 1]]
		#print self.mob.currentRoom	
		winner = self.selector(oddsList)
		#if mob should move, select a random exit and move there
		# print self.mob
		# print Globals.mobsFromFile
		# print self.mob.currentRoom
		# if self.mob.currentRoom != None:
		# 	print "  moveCheck - " + str(self.mob.name) +"["+ str(self.mob.currentRoom.region) + ":" + str(self.mob.currentRoom.name) +"]" + " " + str(winner)
		# else:
		# 	print "  moveCheck - " + str(self.mob.name) + " " + str(winner)
		if winner[0] == 'True' or winner[0] == True:
			# print "winner"
			# print self.mob.currentRoom
			if self.mob.currentRoom != None:
				newRoom = None
				# print "has room"
				randRange = len(self.mob.currentRoom.exits) - 1
				selection = random.randint(0, randRange)
				exitList = []
				for exit in self.mob.currentRoom.exits:
					exitList.append(exit)
				# print exitList

				selectedExit = exitList[selection]
				if self.mob.currentRoom.name == selectedExit:
					selectedExit = None

				for room in Globals.regionListDict[self.mob.currentRoom.region]:
					if Globals.regionListDict[self.mob.currentRoom.region][room].name == selectedExit:
						newRoom = Globals.regionListDict[self.mob.currentRoom.region][room]

				if newRoom != None:				
					for player in self.mob.currentRoom.players:
						player.client.send_cc("^y%s left.^~\n" %self.mob.name.capitalize())

					oldMobRoom = self.mob.currentRoom


					self.mob.currentRoom.mobs.remove(self.mob)
					self.mob.currentRoom = newRoom
					newRoom.mobs.append(self.mob)


				# print oldMobRoom
				# print self.mob.currentRoom
					print "Mm " + str(self.mob) + " " + str(self.mob.name) + ": from [" + str(oldMobRoom.region) +":"+ str(oldMobRoom.name) + "] to [" + str(self.mob.currentRoom.region) +":"+ str(self.mob.currentRoom.name) + "]"

					for player in self.mob.currentRoom.players:
						player.client.send_cc("^yA %s has entered.^~\n" %self.mob.name)

		self.resetTimer()

	def resetTimer(self):
		self.Timer.currentTime = self.time
		# print "resetTimer:" + str(self.Timer) + " " + str(self.Timer.currentTime) + " " + str(self.mob)
		# print Globals.mobsFromFile
		# found = False
		# for mob in Globals.mobsFromFile:
		# 	if mob == self.mob:
		# 		found = True
		# 		print "found " + str(self.mob) + " " + str(mob) 
		# if found == False:
		Globals.MoveTIMERS.append(self.Timer)
		# print "self.mob appended"
		# print Globals.MoveTIMERS