#!/usr/bin/python

import os
import sys
import time
import SharedMem
import Machine
import PLNU_IDCardSwipe
import PipeSwipe
import logging
import MachinePlugCreator
import MakerPassDatabase
import MakerPassLogger

from datetime import datetime
from multiprocessing import Process
from MakerPassLogger import main_logger as logger

## -------global variables---------------------------------

## set controller ID for this controller
MY_MASTER_CONTROLLER_ID = ""


## --------------------------------------------------------
## -------- main ------------------------------------------
## --------------------------------------------------------

def main():

	## print a restarting message...
	logger.debug("\n\n\n\n\t\t\t ---- Restarting MakerPass ------\n\n\n\n")

	## Set up shared mem, default scan_id and machine_id
	logger.debug( "Creating Shared mem" )
	shared_mem = SharedMem.Mem()
	shared_mem.set_shared_mem_values('','')

	## get which cluster controller this is from config
	config_fd = open("cluster_controller.config", "r")
	global MY_MASTER_CONTROLLER_ID
	MY_MASTER_CONTROLLER_ID = config_fd.read().rstrip()
	config_fd.close()

	logger.debug( "Cluster Controller for this machine = " + str(MY_MASTER_CONTROLLER_ID))

	## Create/Init the various machines
	logger.debug( "Instantiating Machine Objects")
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
	
	## main loop
	logger.debug( "Entering main processing loop...")

	## clear feedback on web client
	logUserFeedback("")

	## begin timer for cpu load control
	loop_time_start = datetime.now()

	while (True):	

        	## control loop timing to save CPU from blowing up
		loop_time_end = datetime.now()
      		timediff_millis = (loop_time_end - loop_time_start).total_seconds()

		## quantize loop timing to about 30ms or so
        	if ( timediff_millis <  0.030 ):
		
			time.sleep(0.030 - timediff_millis)
			loop_time_start = datetime.now()

		try:
			
			scan_id = ""
			scanned_username = ""
			selected_machine_id = ""
	
			## retrieve scan/swipe info if a scan has been made
			scan_id, scanner_id = shared_mem.get_shared_mem_values()
		
			## handle a valid scan
			if (scan_id != ""):
				
				logger.debug( "scan_id = " + scan_id)

				## first reset the shared mem, to minimize potential 
				## for failed scans from other machines
				shared_mem.set_shared_mem_values('','')
				scan_id2, scanner_id2 = shared_mem.get_shared_mem_values()	
				
				##  get machine_id from a mapping table of scanner IDs 
				## i.e. map scanning device to machine being scanned to
				selected_machine_id_data = MakerPassDatabase.getMachineId(scanner_id)
				if (selected_machine_id_data == None):
					logger.debug( "Unable to associate a machine with this scanner:  " + scanner_id)
					continue

				## found machine id
				selected_machine_id = selected_machine_id_data['machine_id']
			
				## Get the user associated with this can id
				userinfo = MakerPassDatabase.getUserInfo(scan_id)
				if (userinfo == None):
					logger.debug( "No User found with scan_id = " + str(scan_id))
					continue
				
				## found user
				scanned_username = userinfo['username']
	
				logger.debug( "Scan Detected for User ID: " + str(scan_id))
				logger.debug( "Scanner ID: " + scanner_id)
				logger.debug( "Username = " + scanned_username)
				logger.debug( "Firstname = " + userinfo['firstname'])
				logger.debug( "Lastname = " + userinfo['lastname'])
				logger.debug( "Last Scan = " + userinfo['last_scan'])
				logger.debug( "Total Time Allocated = " + str(userinfo['total_time_allocated']))
				logger.debug( "Total Time Logged = " + str(userinfo['total_time_logged']))
				logger.debug( "") 

				## If no user_machine_allocation_rec (i.e. permission 
				## to the given machine) -- error
				usermachineinfo = MakerPassDatabase.getUserMachineInfo( \
						scanned_username, selected_machine_id)

				if (usermachineinfo == None):
					logUserFeedback("User " + scanned_username + " has no permission to machine: " + selected_machine_id)
					logger.debug( "The given user (" + scanned_username + " )" )
					logger.debug( "has no permission to the given machine (" + selected_machine_id + ")")
					logger.debug( "Please check user_machine_allocation_rec to ensure user")
					logger.debug( "is registered for time on this machine" )
					continue
				
				## If no alloted time left for user (total from user_rec) -- error
				if (userinfo['total_time_logged'] >= userinfo['total_time_allocated']):
					logger.debug( "The given user (%s)" % scanned_username)
					logger.debug( " has exceeded the total alloted to them")
					logger.debug( " for all machines.  Please ensure user record is up to date")
					continue
			
				
                                logger.debug( "Time Allocated for " + selected_machine_id + " = " + str(usermachineinfo['time_allocated']))
                                logger.debug( "Time Logged for " + selected_machine_id + " = " + str(usermachineinfo['time_logged']))

				## If no alloted time left for user on THIS machine 
				## (from user_machine_allocation_rec) -- error
				if (usermachineinfo['time_logged'] >= usermachineinfo['time_allocated']):
					logger.debug( "The given user (%s)" % scanned_username)
					logger.debug( " has no more time left on the scanned machine (%s)" % selected_machine_id)
					continue
			
				## Prevent same user from logging into multiple machines
				if (isUserAlreadyUsingAnotherMachine(scanned_username, selected_machine_id, machine_list)): 
					logger.debug( "You can't do that you're already logged into another machine")
					continue

						

				## display successful swipe and machine selected	
				logger.debug( "User is authorized for machine:  " + selected_machine_id)



			## Now manage each of the machine states
			for machine in machine_list:
			
			
				## pass in scanned user (if any) and which machine was selected
				## to main state handling routines for various machines/plugs
				machine.manageState(scanned_username, selected_machine_id)

                except (KeyboardInterrupt):
						logger.debug("Keyboard Interrupt\n\n")
                        break
                except Exception as ex:
			logger.error("General Exception: \n\n" + ex.message) 
                        break

## --------------------------------------------------------
## this function checks user=machine.user for all machines that do no match 
## selected_machine_id (and not counting blank users)

def isUserAlreadyUsingAnotherMachine(scanned_username, selected_machine_id, machine_list):

	for machine in machine_list:
		if ((machine.machine_id != selected_machine_id) and (scanned_username == machine.current_user)):
			return True

	return False

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
	                
			logger.debug( "Creating machine ID: %s\nPaired With Plug: %s\nPlug IP Address %s\n" % \
				(machine['machine_description'],machine['plug_description']))
			try:

				## First default this machine state to "unrecognized" in the database
				## so we will know if there was an issue initializing (in the web client) 
				MakerPassDatabase.setMachineState(machine['machine_id'], "Unrecognized")

                		new_machine = MachinePlugCreator.instantiateMachinePlug(machine['machine_id'], \
				machine['machine_description'], \
				machine['plug_id'], machine['plug_description'], \
				machine['plug_type'], \
				machine['plug_name'], machine['power_threshold'])

				machine_list.append(new_machine)
				MakerPassDatabase.clearMachineUser(new_machine.machine_id)

			except Exception, ex:
				logger.debug( "Failed to Instantiate machine:  " + machine['machine_description'])
				logger.debug( "Exception:  " + str(ex))
				## continue...non-fatal 

	return machine_list

## --------------------------------------------------------
if __name__ == '__main__': main()

