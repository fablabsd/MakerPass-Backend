#!/usr/bin/python

from getkey import getkey
from MachineStates import MachineStates
from SmartPlug import SmartPlug

class SmartPlugTestBrand(SmartPlug):
        
	def __init__(self, plug_id, description, ip_address):
		super(SmartPlugTestBrand, self).__init__(plug_id, description, ip_address)
		self.switched_on_threshold = 12345  ## need to address what this value should be


        ##  ----- METHODS -------------------------------------
        def enableMachinePlug(self):
                print " SmartPlugTestBrand.enableMachinePlug() called "
        def disableMachinePlug(self):
                print " SmartPlugTestBrand.disableMachinePlug() called "
        def isMachinePlugEnabled(self):
                print " SmartPlugTestBrand.isMachinePlugPlugEnabled() called "
        def isSwitchedOn(self):

		try:

	                fd = open("switch_machine_on","r+")
                	if (fd != None):
                        	fd.close()
				return True

		except IOError:
			pass

		return False

	def manageState(self, scan_detected, is_new_user):

		if (self.state == MachineStates.STATE_ALL_OFF):
	
			if (is_new_user == True): 
				print "plug_id:  " + self.plug_id + " - " + self.ip_address 
				print "Transition to STATE_NEED_SWITCH_ON\n"
				self.state = MachineStates.STATE_NEED_SWITCH_ON
			
			elif (self.isSwitchedOn()): 
				self.state = MachineStates.STATE_NEED_ENABLE
				print "plug_id:  " + self.plug_id + " - " + self.ip_address 
				print "Transition to STATE_NEED_ENABLE\n"
	
	
		elif (self.state == MachineStates.STATE_NEED_SWITCH_ON):
	
			if (self.isSwitchedOn()):
				self.enableMachinePlug()
				self.state = MachineStates.STATE_ALL_ON
				print "plug_id:  " + self.plug_id + " - " + self.ip_address 
				print "Transition to STATE_ALL_ON\n"

			## detect new user
			elif (scan_detected == True): 
				
				## detect an "unswipe"
				if (is_new_user == False): 
					self.state = MachineStates.STATE_ALL_OFF;
					print "plug_id:  " + self.plug_id + " - " + self.ip_address 
					print "Transition to STATE_ALL_OFF\n"


		elif (self.state == MachineStates.STATE_NEED_ENABLE):	
	
			if ( is_new_user == True ): 
				self.enableMachinePlug()
				self.state = MachineStates.STATE_ALL_ON
				print "plug_id:  " + self.plug_id + " - " + self.ip_address 
				print "Transition to STATE_ALL_ON\n"
			
			elif (not(self.isSwitchedOn())): 
				self.state = MachineStates.STATE_ALL_OFF
				print "plug_id:  " + self.plug_id + " - " + self.ip_address 
				print "Transition to STATE_ALL_OFF\n"
		

		elif (self.state == MachineStates.STATE_ALL_ON):
	
			## note there is no "unswipe" option here - we do not
			## automatically switch off a machine  - user must turn
			## it off and then they will be automatically logged out
			if (not(self.isSwitchedOn())): 
				self.state = MachineStates.STATE_ALL_OFF
				self.disableMachinePlug()
				print "plug_id:  " + self.plug_id + " - " + self.ip_address 
				print "Transition to STATE_ALL_OFF\n"

		else: 
			print "StatePlugWemoInsight.manageState():  oops..invalid state encountered..."
			print " must have been those darn cosmic rays.."
			raise SystemExit
	

import termios, sys, os
#import termios, TERMIOS, sys, os
TERMIOS = termios
def getkey():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
        new[6][TERMIOS.VMIN] = 1
        new[6][TERMIOS.VTIME] = 0
        termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
        c = None
        try:
                c = os.read(fd, 1)
        finally:
                termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
        return c
	

