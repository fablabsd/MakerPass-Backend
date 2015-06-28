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
		logged_out_user = ""
		need_record_time_used = False
		clear_current_user_from_db = False

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
					
					## set to record logged time of the user being logged out if applicable i.e.
					## this is for the case where we are replacing the current user with another
					## while the machine is on
					if (self.state == MachineStates.STATE_ALL_ON):
						need_record_time_used = True
						logged_out_user = self.current_user

	                                ## Update last scan time in user_rec and user_machine_allocation_rec
                                	## and register a scan in user_scan_rec
                                	logger.debug( "Registering scan in for user: " + scanned_user)
                                	MakerPassDatabase.updateUserScanRecords(scanned_user, selected_machine_id)

					## set the current user
					logger.debug( "Setting current user:")
					logger.debug( "User = " + scanned_user)
					logger.debug( "Machine = " + selected_machine_id)
					self.current_user = scanned_user
					
		## now enter main state management for the plug to determine
		## if it should be enabled or not 
		self.doManageState(scan_detected, is_new_user)

		## if state changed, log it so we can see it in the heads-up display
		if (self.state != prev_state):
			MakerPassDatabase.setMachineState(self.machine_id, MachineStates.toString(self.state))
		

		## mark machine effective use time - this is the time the machine has actually been switched on
		## we do this so the user is not charged for time between when they scanned and the machine was turned on
		if ((self.state == MachineStates.STATE_ALL_ON) and (prev_state != MachineStates.STATE_ALL_ON)):
			MakerPassDatabase.markMachineEffectiveUseTime(self.current_user, self.machine_id)

		## if we just transitioned to all off from all on then indicate need to record time used from prev user
		if ((self.state == MachineStates.STATE_ALL_OFF) and (prev_state == MachineStates.STATE_ALL_ON)):
			need_record_time_used = True
                        logged_out_user = self.current_user
			clear_current_user_from_db = True

		## if the current state is ALL_OFF, and the user is set, then we just transitioned to ALL_OFF
		## so reset the user 
		if ((self.state == MachineStates.STATE_ALL_OFF) and (self.current_user != "")):
                        self.current_user = ""
			clear_current_user_from_db = True

		## clear the current user from the machine in the database
		if (clear_current_user_from_db == True):
			MakerPassDatabase.clearMachineUser(self.machine_id)
	
		## set time_logged in database for the previous user if applicable 	
		if (need_record_time_used == True):
			##  record/subtract time used
                        logger.debug( "Recording time used for user:")
                        logger.debug( "User = " + logged_out_user)
                        logger.debug( "Machine = " + self.machine_description)
			if (self.current_user == ""):
				clear_current_user_from_db = True
				
                        MakerPassDatabase.recordTimeUsed(logged_out_user, self.machine_id, clear_current_user_from_db)
