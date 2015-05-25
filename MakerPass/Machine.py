#!/usr/bin/python

import sys
import SmartPlugWemoInsight
import SmartPlugTestBrand

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

		## only operate on scanned user if they scanned into this machine
		if (selected_machine_id == self.machine_id):

			## need to know if scan was detected so we can determine if
			## this is a scan out or a new scanned user
			if (scanned_user != ""): 
				scan_detected = True
				## determine if this is a new scanned user 
				if (scanned_user != self.current_user):
					self.current_user = scanned_user
					is_new_user = True				
					 
		self.plug.manageState(scan_detected, is_new_user)

		## if we just transitioned into the ALL_OFF state then record
		## the time used for this user, and reset the user
		if ((self.plug.state == MachineStates.STATE_ALL_OFF) and (prev_state != MachineStates.STATE_ALL_OFF)):
			## TBD:  record/subtract time used
			self.current_user = ""

