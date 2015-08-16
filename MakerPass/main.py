#!/usr/bin/python

import os
import sys
import time
import SharedMem
import PLNU_IDCardSwipe
import PipeSwipe
import WifiSwipe
import logging
import MachinePlugCreator
import MakerPassDatabase
import MakerPassLogger

from datetime import datetime
from multiprocessing import Process
from MakerPassLogger import main_logger as logger
from MachineStates import MachineStates
from RegisterScan import registerScan

## -------global variables---------------------------------

## set controller ID for this controller
MY_MASTER_CONTROLLER_ID = ""
shared_mem = ""
machine_list = ""
scanned_username = ""
selected_machine_id = ""
loop_time_start = ""


## --------------------------------------------------------
## -------- main ------------------------------------------
## --------------------------------------------------------

def main():

	## print a restarting message...
	logger.debug("\n\n\n\n\t\t\t ---- Restarting MakerPass ------\n\n\n\n")


	## init shared mem, machines etc
	initMakerPass()


	## begin timer for cpu load control
	global loop_time_start
	loop_time_start = datetime.now()
	
	## main loop
	logger.debug( "Entering main processing loop...")
	while (True):	

		limitLoopFrameRate()

		try:
		
			scanned_username = ""
			selected_machine_id = ""
			client_ip = ""

		        ## retrieve scan/swipe info from shared mem if a scan has been made
        		scan_id, scanner_id, client_ip, need_auth = shared_mem.get_shared_mem_values()

			## validate scan and retrieve user+machine if necessary 
			if (need_auth == "True"):
				ret_val, scanned_username, selected_machine_id = registerScan(scan_id, scanner_id)
                	else:
				## if shared mem values were already registered, then assume they hold
				## valid user+machine
				ret_val = 0
				scanned_username = scan_id
				selected_machine_id = scanner_id
	
			## reset shared mem
                	shared_mem.set_shared_mem_values('','','','')
                	dummy1,dummy2,dummy3,dummy4 = shared_mem.get_shared_mem_values()
			
			if (ret_val == -1): 
				## we have the option of sending feedback to the scanner in event
				## of failed scan registration -- do so here, and then continue event
				## loop
				logger.debug("Failed scan from IP: " + str(client_ip))
				if (client_ip != "0.0.0.0"):
					logger.debug("sending failed string to scanner")
					## TBD:  send failed string to scanner endpoint
					
				continue  ##
			else:
				## send success feedback if a scan was made
				if (scanned_username != ""):
					logger.debug("Successful scan from IP: " + str(client_ip))
					if (client_ip != "0.0.0.0"):
						logger.debug("sending success string to scanner")
						## TBD:  send success string to scanner endpoint

						
			## Now manage each of the machine states
			for machine in machine_list:
				## pass in scanned user (if any) and which machine was selected
				## to main state handling routines for various machines/plugs
				machine.manageState(scanned_username, selected_machine_id)

		except (KeyboardInterrupt):
			logger.debug("Keyboard Interrupt\n\n")
			sys.exit(0)
		except Exception as ex:
			logger.error("General Exception: \n\n" + ex.message) 
			sys.exit(1)


## --------------------------------------------------------
## prevent CPU from loading too much, by limiting execution
## time of main loop
def limitLoopFrameRate():

	global loop_time_start
	
	## control loop timing to save CPU from blowing up
	loop_time_end = datetime.now()
	timediff_millis = (loop_time_end - loop_time_start).total_seconds()
	#logger.debug("timediff_millis = " + str(timediff_millis))

	## quantize loop timing to about 60ms or so
	if ( timediff_millis <  0.060 ):
		time.sleep(0.060 - timediff_millis)
		
	## restart timer
	loop_time_start = datetime.now()
		
		
## --------------------------------------------------------
## perform general initialization before program main loop
##

def initMakerPass():

	
	## Set up shared mem, default scan_id and machine_id
	logger.debug( "Creating Shared mem" )
	global shared_mem
	shared_mem = SharedMem.Mem()
	shared_mem.set_shared_mem_values('','','','')

	## get which cluster controller this is from config
	config_fd = open("cluster_controller.config", "r")
	global MY_MASTER_CONTROLLER_ID
	MY_MASTER_CONTROLLER_ID = config_fd.read().rstrip()
	config_fd.close()

	logger.debug( "Cluster Controller for this machine = " + str(MY_MASTER_CONTROLLER_ID))

	## Create/Init the various machines
	logger.debug( "Instantiating Machine Objects")
	global machine_list
	machine_list = InitMachines(shared_mem)

	## make sure we actually successfully retrieved machine definitions
	## from databse before continuing
	if (len(machine_list) == 0):
		logger.debug( "No machine definitions were retrieved from database...exiting")
		sys.exit()
	
	## Spawn any/all scan device processes which will use
	## the shared mem to populate a scan  
	logger.debug( "Spawning PLNU magstripe handler process")
    	Process(target=PLNU_IDCardSwipe.main, args=(shared_mem,"PLNU_MAG_SWIPE")).start()
    	logger.debug( "Spawning Pipe scan handler process")
    	Process(target=PipeSwipe.main, args=(shared_mem, "null")).start()
    	logger.debug( "Spawning Wifi pipe scan handler process")
    	Process(target=WifiSwipe.main, args=(shared_mem, "null")).start()

	## clear feedback on web client
	logUserFeedback("")
	
	


## --------------------------------------------------------
## Respond to web client with this feedback
		
def logUserFeedback(feedbackString):
	feedback_file = open('cgi/user_feedback.txt', "w")
        feedback_file.write(feedbackString)
        feedback_file.close()


## --------------------------------------------------------

def InitMachines(shared_mem):

	machine_list = []

	## get machine ids from database
	rows = MakerPassDatabase.getMachineRecords()

	## Create machine object for each machine
	## that belongs to this master controller  
	#for machine_id in machine_ids:
	for machine in rows:  
	
		## ignore this machine definition if I'm not the master/owner
		## i.e. support clustering of master/owner controllers paired to 
		## a list of child/owned machines

		if (machine['parent_machine_id'] == MY_MASTER_CONTROLLER_ID ):
	                
			logger.debug( "Creating machine ID: %s\nPaired With Plug: %s\n" % \
				(machine['machine_description'],machine['plug_description']))
			try:

				## First default this machine state to "unrecognized" in the database
				## so we will know if there was an issue initializing (in the web client) 
				MakerPassDatabase.setMachineState(machine['machine_id'], "Unrecognized")
			
				## clear out any pre-existing users this machine might have had on last exit	
				MakerPassDatabase.clearMachineUser(machine['machine_id'])

				## clear out any pre-existing user feedback messages for this machine 
				MakerPassDatabase.clearMachineLastMessage(machine['machine_id'])

				## instantiate the machine
                		new_machine = MachinePlugCreator.instantiateMachinePlug(machine['machine_id'], \
				machine['machine_description'], \
				machine['plug_id'], machine['plug_description'], \
				machine['plug_type'], \
				machine['plug_name'], machine['power_threshold'])

				## add machine to list of machines to run through update loop
				machine_list.append(new_machine)

				## update the database to reflect default state (we must do this 
				## after the machine is fully instantiated so we know it's valid)
				MakerPassDatabase.setMachineState(new_machine.machine_id, MachineStates.toString(new_machine.state))
				

			except Exception, ex:
				logger.debug( "Failed to Instantiate machine:  " + machine['machine_description'])
				logger.debug( "Exception:  " + str(ex))
				## continue...non-fatal 

	return machine_list

## --------------------------------------------------------
if __name__ == '__main__': main()

