#!/usr/bin/python


import ouimeaux

from MachinePlug_PowerMonitored import MachinePlug_PowerMonitored
from MachineStates import MachineStates
from datetime import datetime
from ouimeaux.environment import Environment
from ouimeaux.environment import UnknownDevice
from MakerPassLogger import MachinePlug_WemoInsight_logger as logger

class MachinePlug_WemoInsight(MachinePlug_PowerMonitored):

	## static instance of the wemo environment
	env = 0
        
	def __init__(self, machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold):
		super(MachinePlug_WemoInsight, self).__init__(machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold)

		## create the static/global WEMO environment variable if it doesn't exist
		if (MachinePlug_WemoInsight.env == 0):
			MachinePlug_WemoInsight.env = Environment(with_cache=False, bind=None)
			MachinePlug_WemoInsight.env.start()
        		MachinePlug_WemoInsight.env.discover(3)
			
		self.wemo_switch = self.getSwitch(plug_name)
		logger.debug( "switch = " + str(self.wemo_switch))




        ##  ----- METHODS -------------------------------------

	def getSwitch(self, plug_name):
		try:
			return MachinePlug_WemoInsight.env.get_switch(plug_name)
		except (UnknownDevice):
			logger.debug( "Unable to get switch:  " + self.plug_name)
			raise UnknownDevice
			

        def doEnableMachinePlug(self):
                logger.debug( " MachinePlug_WemoInsight.doEnableMachinePlug() called ")
		self.wemo_switch.basicevent.SetBinaryState(BinaryState=1)
        def doDisableMachinePlug(self):
                logger.debug( " MachinePlug_WemoInsight.doDisableMachinePlug() called ")
		self.wemo_switch.basicevent.SetBinaryState(BinaryState=0)


	def doIsPowerAboveThreshold(self):

		power = self.wemo_switch.current_power
		logger.debug( "power for " + self.plug_name + ": " + str(power))
			
		if (power > self.machine_power_threshold):
			return True

                return False
		
	

	

