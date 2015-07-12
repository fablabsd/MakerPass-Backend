#!/usr/bin/python

import sys
import MachinePlug_WemoInsight
import MachinePlug_TestBrand
import MachinePlug_GPIO

from MakerPassLogger import MachinePlugCreator_logger as logger
	
##class MachinePlugCreator(object):


def instantiateMachinePlug(machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold): 


	## instantiate the appropriate plug handler for this Machine
	if (plug_type == "WEMO_INSIGHT"):
		logger.debug( "Instantiating a WEMO_INSIGHT machine\n")
		return  MachinePlug_WemoInsight.MachinePlug_WemoInsight(machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold)
	elif (plug_type == "TEST_BRAND"):
		logger.debug( "Instantiating a TEST_BRAND machine\n")
		return  MachinePlug_TestBrand.MachinePlug_TestBrand(machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold)
	elif (plug_type == "GPIO"):
		logger.debug( "Instantiating a GPIO machine\n")
		return  MachinePlug_GPIO.MachinePlug_GPIO(machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold)
	else:
		logger.debug( "FATAL:  Invalid plug_type received: " + plug_type)
		raise SystemExit

