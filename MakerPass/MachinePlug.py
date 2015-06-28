#!/usr/bin/python

import sys
import MakerPassDatabase

from MachineStates import MachineStates
from MakerPassLogger import MachinePlug_logger as logger
	
class MachinePlug(object):


	def __init__(self, machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold):

		## set member properties
		self.machine_id = machine_id
		self.machine_description = machine_desc
		self.current_user = ""

		self.plug_id = plug_id
		self.plug_desc = plug_desc
		self.state = MachineStates.STATE_ALL_OFF
                
		## unique name of the plug, used to 
		## determine what plug to connect to (i.e. it's loaded into the plug beforehand) 
		self.plug_name = plug_name

		## used to determine whether machine is switch one - in milliwatts
		self.machine_power_threshold = machine_power_threshold

		## update the database to reflect default state (for cases where 
		## we just restarted and state is out of sync)
		MakerPassDatabase.setMachineState(self.machine_id, MachineStates.toString(self.state))
	
	def manageState(self, scanned_user, selected_machine_id):

		scan_detected = False
		is_new_user = False
		prev_state = self.state

		## only operate on scanned user if they scanned into this machine
		if (selected_machine_id == self.machine_id):

			## need to know if scan was detected so we can determine if
			## this is a scan out or a new scanned user
			if (scanned_user != ""): 

				scan_detected = True

				## determine if this is a new scanned user -- this empowers scan-outs since
				## a scan-out will involve a scan_detected, but no new user 
				if (scanned_user != self.current_user):
					
					is_new_user = True	
					self.newUserScanIn(scanned_user, selected_machine_id)			
					
		## now enter main state management for the plug to determine
		## if it should be enabled or not 
		self.doManageState(scan_detected, is_new_user)

	def newUserScanIn(self, scanned_user, selected_machine_id):

		## set to record logged time of the user being logged out if applicable i.e.
		## this is for the case where we are replacing the current user with another
		## while the machine is on
		if (self.state == MachineStates.STATE_ALL_ON):
			MakerPassDatabase.logoutUser(self.current_user, self.machine_id)

		## Update last scan time in user_rec and user_machine_allocation_rec
		## and register a scan in user_scan_rec
		logger.debug( "Registering scan in for user: " + scanned_user)
		MakerPassDatabase.loginUser(scanned_user, selected_machine_id)

		## set the current user
		logger.debug( "Setting current user:")
		logger.debug( "User = " + scanned_user)
		logger.debug( "Machine = " + selected_machine_id)
		self.current_user = scanned_user
					

	

