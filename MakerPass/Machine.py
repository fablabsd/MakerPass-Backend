#!/usr/bin/python

import sys
import SmartPlugWemoInsight
import SmartPlugTestBrand
import MakerPassDatabase

from MachineStates import MachineStates
	
class Machine(object):


	def __init__(self, machine_id, machine_desc, plug_id, plug_desc, plug_ip_addr, plug_type):
		self.machine_id = machine_id
		self.machine_description = machine_desc
		self.current_user = ""

		if (plug_type == "WEMO_INSIGHT"):
			self.plug = SmartPlugWemoInsight.SmartPlugWemoInsight(plug_id, plug_desc,plug_ip_addr)
		elif (plug_type == "TEST_BRAND"):
			self.plug = SmartPlugTestBrand.SmartPlugTestBrand(plug_id, plug_desc,plug_ip_addr)
		else:
			print "FATAL:  Invalid plug_type received: " + plug_type
			raise SystemExit
	
	def manageState(self, scanned_user, selected_machine_id):

		scan_detected = False
		is_new_user = False
		prev_state = self.plug.state
		logged_out_user = ""
		need_record_time_used = False

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
					if (self.plug.state == MachineStates.STATE_ALL_ON):
						need_record_time_used = True
						logged_out_user = self.current_user

	                                ## Update last scan time in user_rec and user_machine_allocation_rec
                                	## and register a scan in user_scan_rec
                                	print "Registering scan in for user: " + scanned_user
                                	MakerPassDatabase.updateUserScanRecords(scanned_user, selected_machine_id)

					## set the current user
					print "Setting current user:"
					print "User = " + scanned_user
					print "Machine = " + selected_machine_id
					self.current_user = scanned_user
					
		## now enter main state management for the plug to determine
		## if it should be enabled or not 
		self.plug.manageState(scan_detected, is_new_user)

		## mark machine effective use time - this is the time the machine has actually been switched on
		## we do this so the user is not charged for time between they scanned and the machine was turned on
		if ((self.plug.state == MachineStates.STATE_ALL_ON) and (prev_state != MachineStates.STATE_ALL_ON)):
			MakerPassDatabase.markMachineEffectiveUseTime(self.current_user, self.machine_id)

		## if we just transitioned to all off from all on then indicate need to record time used from prev user
		if ((self.plug.state == MachineStates.STATE_ALL_OFF) and (prev_state == MachineStates.STATE_ALL_ON)):
			need_record_time_used = True
                        logged_out_user = self.current_user

		## if the current state is ALL_OFF, and the user is set, then we just transitioned to ALL_OFF
		## so reset the user 
		if ((self.plug.state == MachineStates.STATE_ALL_OFF) and (self.current_user != "")):
                        self.current_user = ""
	
		## set time_logged in database for the previous user if applicable 	
		if (need_record_time_used == True):
			##  record/subtract time used
                        print "Recording time used for user:"
                        print "User = " + logged_out_user
                        print "Machine = " + self.machine_description
                        MakerPassDatabase.recordTimeUsed(logged_out_user, self.machine_id)
