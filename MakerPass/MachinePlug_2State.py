#!/usr/bin/python

import MakerPassDatabase

from MachinePlug import MachinePlug
from MachineStates import MachineStates
from datetime import datetime
from MakerPassLogger import MachinePlug_2State_logger as logger


class MachinePlug_2State(MachinePlug):

	def __init__(self, machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold):
		super(MachinePlug_2State, self).__init__(machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold)

		## we delay calls to isSwitchedOn() to reduce network overhead -- these
		## vars help us perform timeouts -- we re-mark this time when leaving ALL_OFF state
		self.switched_off_timeout_start = datetime.now()

		## amount of time we wait before cutting power to machine
		self.switched_off_delay_time = 60
	

        ##  ----- METHODS -------------------------------------


        def enableMachinePlug(self):
                logger.debug( " MachinePlug_2State.enableMachinePlug() called ")
		self.doEnableMachinePlug()
        def disableMachinePlug(self):
                logger.debug( " MachinePlug_2State.disableMachinePlug() called ")
		self.doDisableMachinePlug()



	def doManageState(self, scan_detected, is_new_user):


		if (self.state == MachineStates.STATE_ALL_OFF):

			## machine and plug are both off in this state
			## so we are just waiting for a scan
			if (is_new_user == True): 
				logger.debug( "plug_id:  " + self.plug_id  )
				logger.debug( "Transition to STATE_ALL_ON\n")
				self.enableMachinePlug()
				self.state = MachineStates.STATE_ALL_ON
				MakerPassDatabase.setMachineState(self.machine_id, MachineStates.toString(self.state))
			
	
		elif (self.state == MachineStates.STATE_ALL_ON):
	
                        ## detect an unswipe of the same user (not need to detect a different user)
                        if (scan_detected == True):

                                if (is_new_user == False):
                                        logger.debug( "plug_id:  " + self.plug_id)
                                        logger.debug( "Transition to STATE_NEED_SWITCH_OFF\n")
                                        self.state = MachineStates.STATE_NEED_SWITCH_OFF;
                                	MakerPassDatabase.logoutUser(self.current_user, self.machine_id)
                                        MakerPassDatabase.clearMachineUser(self.machine_id)
                                        MakerPassDatabase.setMachineState(self.machine_id, MachineStates.toString(self.state))
                                        self.current_user = ""
					## mark begin time for timeout of machine disable
					self.switched_off_timeout_start = datetime.now()
					self.logUserFeedback("Turning off " + self.plug_id + " in 1 min<br>please ensure machine is switched off")

                elif (self.state == MachineStates.STATE_NEED_SWITCH_OFF):

			## in this state, we are just waiting a short period to give the user 
			## a chance to power of the machine manually before we disable the plug
	                
			## calculate how long since last check
                	switch_off_timeout_end = datetime.now()
                	timediff_millis = (switch_off_timeout_end - self.switched_off_timeout_start).total_seconds()
                	if ( timediff_millis > self.switched_off_delay_time ):
                        	logger.debug( "Switching off (" + self.machine_id + ") after delay:  %.2gs" % timediff_millis)
                                logger.debug( "plug_id:  " + self.plug_id  )
                                logger.debug( "Transition to STATE_ALL_OFF\n")
                                self.state = MachineStates.STATE_ALL_OFF
                                MakerPassDatabase.setMachineState(self.machine_id, MachineStates.toString(self.state))
                                self.disableMachinePlug()

		else: 
			logger.debug( "MachinePlug_2State.doManageState():  oops..invalid state encountered...")
			logger.debug( " must have been those darn cosmic rays..")
			raise SystemExit
	

	
	## --------------------------------------------------------
	## Respond to web client with this feedback

	def logUserFeedback(self, feedbackString):
        	feedback_file = open('cgi/user_feedback.txt', "w")
        	feedback_file.write(feedbackString)
        	feedback_file.close()

