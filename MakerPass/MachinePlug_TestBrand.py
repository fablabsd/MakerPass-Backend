#!/usr/bin/python

import MachinePlug_PowerMonitored

from MachinePlug_PowerMonitored import MachinePlug_PowerMonitored
from MachineStates import MachineStates
from datetime import datetime
from MakerPassLogger import MachinePlug_TestBrand_logger as logger

class MachinePlug_TestBrand(MachinePlug_PowerMonitored):

	## static instance of the wemo environment
	env = 0
        
	def __init__(self, machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold):
		super(MachinePlug_TestBrand, self).__init__(machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold)

		

        ##  ----- METHODS -------------------------------------

	
        def doEnableMachinePlug(self):
                logger.debug( " MachinePlug_TestBrand.doEnableMachinePlug() called ")

        def doDisableMachinePlug(self):
                logger.debug( " MachinePlug_TestBrand.doDisableMachinePlug() called ")


	def doIsPowerAboveThreshold(self):

                try:

                        fd = open("switch_machine_on","r+")
                        if (fd != None):
                                fd.close()
                                return True

                except IOError:
                        pass

                return False		
	

	

