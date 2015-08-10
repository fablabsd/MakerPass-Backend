#!/usr/bin/python

import os
import sys
import time
import SharedMem
import PLNU_IDCardSwipe
import PipeSwipe
import logging
import MachinePlugCreator
import MakerPassDatabase
import MakerPassLogger

from datetime import datetime
from multiprocessing import Process
from MakerPassLogger import main_logger as logger
from MachineStates import MachineStates

## -------global variables---------------------------------

## set controller ID for this controller
MY_MASTER_CONTROLLER_ID = ""
shared_mem = ""
machine_list = ""
scanned_username = ""
selected_machine_id = ""
client_ip = ""
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
		
			global scanned_username
			global selected_machine_id
			global client_ip
			
			scanned_username = ""
			selected_machine_id = ""
			client_ip = ""
	
			## retrieve and validate any potential scan from 
			## shared mem
			ret_val = registerScan()
			if (ret_val == -1): 
				## we have the option of sending feedback to the scanner in event
				## of failed scan registration -- do so here, and then continue event
				## loop
				logger.debug("Failed scan from IP: " + str(client_ip))
				if (client_ip != "0.0.0.0"):
					logger.debug("sending failed string to scanner")
					
				continue  ##
			else:
				## send success feedback if a scan was made
				if (scanned_username != ""):
					logger.debug("Successful scan from IP: " + str(client_ip))
					if (client_ip != "0.0.0.0"):
						logger.debug("sending success string to scanner")

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
## Read and validate a scan input from various sources into
## shared mem

def registerScan():

	global scanned_username
	global selected_machine_id 
	global client_ip 

	scan_id = ""
	scanner_id = ""
	
	## retrieve scan/swipe info if a scan has been made
	scan_id, scanner_id, client_ip = shared_mem.get_shared_mem_values()

	## handle a valid scan
	if (scan_id != ""):
		
		logger.debug( "scan_id = " + scan_id)
		logger.debug( "scanner_id = " + scanner_id)
		logger.debug( "client_ip = " + client_ip)

		## first reset the shared mem, to minimize potential 
		## for failed scans from other machines
		shared_mem.set_shared_mem_values('','','')
		scan_id_dummy, scanner_id_dummy, client_id_dummy = shared_mem.get_shared_mem_values()	
		
		##  get machine_id from a mapping table of scanner IDs 
		## i.e. map scanning device to machine being scanned to
		selected_machine_id_data = MakerPassDatabase.getMachineId(scanner_id)
		if (selected_machine_id_data == None):
			logger.debug( "Unable to associate a machine with this scanner:  " + scanner_id)
			logUserFeedback( "Unable to associate a machine with this scanner:  " + scanner_id)
			return -1

		## found machine id
		selected_machine_id = selected_machine_id_data['machine_id']
	
		## Get the user associated with this scan id
		userinfo = MakerPassDatabase.getUserInfo(scan_id)
		if (userinfo == None):
			logger.debug( "No User found with scan_id = " + str(scan_id))
			logUserFeedback( "No User found with scan_id = " + str(scan_id))
			MakerPassDatabase.setLastMessage( "No User found with scan_id = " + str(scan_id), selected_machine_id)
			return -1
		
		## found user
		scanned_username = userinfo['username']

		logger.debug( "Scan Detected for User ID: " + str(scan_id))
		logger.debug( "Scanner ID: " + scanner_id)
		logger.debug( "Username = " + scanned_username)
		logger.debug( "Firstname = " + userinfo['firstname'])
		logger.debug( "Lastname = " + userinfo['lastname'])
		logger.debug( "Last Scan = " + str(userinfo['last_scan']))
		logger.debug( "Total Time Allocated = " + str(userinfo['total_time_allocated']))
		logger.debug( "Total Time Logged = " + str(userinfo['total_time_logged']))
		logger.debug( "") 

		## If no user_machine_allocation_rec (i.e. permission 
		## to the given machine) -- error
		usermachineinfo = MakerPassDatabase.getUserMachineInfo( \
				scanned_username, selected_machine_id)

		if (usermachineinfo == None):
			logUserFeedback("User " + userinfo['firstname'] + " " + userinfo['lastname'] + " has no permission to machine: " + selected_machine_id)
			logger.debug( "The given user (" + scanned_username + " )" )
			logger.debug( "has no permission to the given machine (" + selected_machine_id + ")")
			logger.debug( "Please check user_machine_allocation_rec to ensure user")
			logger.debug( "is registered for time on this machine" )
			MakerPassDatabase.setLastMessage( "Access Denied to: " + scanned_username, selected_machine_id)
			return -1
		
		## If no alloted time left for user (total from user_rec) -- error
		if (userinfo['total_time_logged'] >= userinfo['total_time_allocated']):
			logger.debug( "The given user (%s)" % scanned_username)
			logger.debug( " has exceeded the total alloted to them")
			logger.debug( " for all machines.  Please ensure user record is up to date")
			logUserFeedback("User " +  userinfo['firstname'] + " " + userinfo['lastname']  + " Exceeded total time allotment - see administrator for details")
			MakerPassDatabase.setLastMessage( "Total allotted time exceeded for: " + scanned_username, selected_machine_id)
			return -1
	
		
		logger.debug( "Time Allocated for " + selected_machine_id + " = " + str(usermachineinfo['time_allocated']))
		logger.debug( "Time Logged for " + selected_machine_id + " = " + str(usermachineinfo['time_logged']))

		## If no alloted time left for user on THIS machine 
		## (from user_machine_allocation_rec) -- error
		if (usermachineinfo['time_logged'] >= usermachineinfo['time_allocated']):
			logger.debug( "The given user (%s)" % scanned_username)
			logger.debug( " has no more time left on the scanned machine (%s)" % selected_machine_id)
			logUserFeedback("User " +  userinfo['firstname'] + " " + userinfo['lastname']  + " Exceeded time allotment on the given machine - see administrator for details")
			MakerPassDatabase.setLastMessage( "Allotted time exceeded on this machine for: " + scanned_username, selected_machine_id)
			return -1
	
		## Prevent same user from logging into multiple machines
		if (isUserAlreadyUsingAMachine(scanned_username, selected_machine_id, machine_list)): 
			logger.debug( "You can't do that you're already logged into a machine")
			logUserFeedback("User " +  userinfo['firstname'] + " " + userinfo['lastname']  + " is already logged into another machine")
			MakerPassDatabase.setLastMessage( "This user already using another machine: " + scanned_username, selected_machine_id)
  			return -1

				

		## display successful swipe and machine selected	
		logger.debug( "User is authorized for machine:  " + selected_machine_id)
		logUserFeedback("Successfully scanned " +  userinfo['firstname'] + " " + userinfo['lastname']  + " for machine:  " + selected_machine_id)
		
		return 0



## --------------------------------------------------------
## perform general initialization before program main loop
##

def initMakerPass():

	
	## Set up shared mem, default scan_id and machine_id
	logger.debug( "Creating Shared mem" )
	global shared_mem
	shared_mem = SharedMem.Mem()
	shared_mem.set_shared_mem_values('','','')

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

	## clear feedback on web client
	logUserFeedback("")
	
	


## --------------------------------------------------------
## this function checks user=machine.user for all machines  
## to ensure no attempt is made to log user in multiple machines

def isUserAlreadyUsingAMachine(scanned_username, selected_machine_id, machine_list):

	## see if user is attempting to login to a machine other than the one they are
	## already logged in to - we don't care about the one they are logged in to because
	## we allow for un-scanning from their current machine
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

