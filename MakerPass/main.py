#!/usr/bin/python

import os
import sys
import time
import SharedMem
import Machine
import PLNU_IDCardSwipe
import PipeSwipe
import MakerPassDatabase

from datetime import datetime
from multiprocessing import Process


## -------global variables---------------------------------

## set controller ID for this controller
#MY_MASTER_CONTROLLER_ID = os.environ["MY_MASTER_CONTROLLER_ID"]
MY_MASTER_CONTROLLER_ID = ""


## --------------------------------------------------------
## -------- main ------------------------------------------
## --------------------------------------------------------

def main():

	## Set up shared mem, default scan_id and machine_id
	print "Creating Shared mem" 
	shared_mem = SharedMem.Mem()
	shared_mem.set_shared_mem_values('','')

        ## get which cluster controller this is from config
        config_fd = open("cluster_controller.config", "r")
        global MY_MASTER_CONTROLLER_ID
        MY_MASTER_CONTROLLER_ID = config_fd.read().rstrip()
        config_fd.close()

	print "Cluster Controller for this machine = " + MY_MASTER_CONTROLLER_ID

	## Create/Init the various machines
	print "Instantiating Machine Objects"
	machine_list = InitMachines(shared_mem)

	## make sure we actually successfully retrieved machine definitions
	## from databse before continuing
	if (len(machine_list) == 0):
		print "No machine definitions were retrieved from database...exiting"
		sys.exit()
	
	## Spawn any/all scan device processes which will use
	## the shared mem to populate a scan  
        print "Spawning PLNU magstripe handler process";
        Process(target=PLNU_IDCardSwipe.main, args=(shared_mem,"PLNU_MAG_SWIPE")).start()
        print "Spawning Pipe scan handler process";
        Process(target=PipeSwipe.main, args=(shared_mem, "null")).start()
	
	## main loop
	print "Entering main processing loop..."

	
	loop_time_start = datetime.now()

	while (True):	

                ## control loop timing to save CPU from blowing up
                loop_time_end = datetime.now()
        	timediff_millis = (loop_time_end - loop_time_start).total_seconds()

		#print "sleeping - timediff = " + str(timediff_millis)

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
				
				print "scan_id = " + scan_id

				## first reset the shared mem, to minimize potential 
				## for failed scans from other machines
				shared_mem.set_shared_mem_values('','')
				scan_id2, scanner_id2 = shared_mem.get_shared_mem_values()	
				
				##  get machine_id from a mapping table of scanner IDs 
				## i.e. map scanning device to machine being scanned to
				selected_machine_id_data = MakerPassDatabase.getMachineId(scanner_id)
				if (selected_machine_id_data == None):
					print "Unable to associate a machine with this scanner:  " + scanner_id
					continue

				## found machine id
				selected_machine_id = selected_machine_id_data['machine_id']
			
				## Get the user associated with this can id
				userinfo = MakerPassDatabase.getUserInfo(scan_id)
				if (userinfo == None):
					print "No User found with scan_id = " + str(scan_id)	
					continue
				
				## found user
				scanned_username = userinfo['username']
			
				print "Scan Detected for User ID: " + str(scan_id)
				print "Scanner ID: " + scanner_id
				print "Username = " + scanned_username
				print "Firstname = " + userinfo['firstname']
				print "Lastname = " + userinfo['lastname']
				print "Last Scan = " + userinfo['last_scan']
				print "Total Time Allocated = " + str(userinfo['total_time_allocated'])
				print "Total Time Logged = " + str(userinfo['total_time_logged'])
				print ""

				## If no user_machine_allocation_rec (i.e. permission 
				## to the given machine) -- error
				usermachineinfo = MakerPassDatabase.getUserMachineInfo( \
						scanned_username, selected_machine_id)

				if (usermachineinfo == None):
					print "The given user (" + scanned_username + " )" 
					print "has no permission to the given machine (" + selected_machine_id + ")"
					print "Please check user_machine_allocation_rec to ensure user"
					print "is registered for time on this machine" 
					continue
				
				## If no alloted time left for user (total from user_rec) -- error
				if (userinfo['total_time_logged'] >= userinfo['total_time_allocated']):
					print "The given user (%s)" % scanned_username
					print " has exceeded the total alloted to them"
					print " for all machines.  Please ensure user record is up to date"
					continue
			
				
                                print "Time Allocated for " + selected_machine_id + " = " + str(usermachineinfo['time_allocated'])
                                print "Time Logged for " + selected_machine_id + " = " + str(usermachineinfo['time_logged'])

				## If no alloted time left for user on THIS machine 
				## (from user_machine_allocation_rec) -- error
				if (usermachineinfo['time_logged'] >= usermachineinfo['time_allocated']):
					print "The given user (%s)" % scanned_username
					print " has no more time left on the scanned machine (%s)" % selected_machine_id
					continue
			
				## Prevent same user from logging into multiple machines
				if (isUserAlreadyUsingAnotherMachine(scanned_username, selected_machine_id, machine_list)): 
					print "You can't do that you're already logged into another machine"
					continue

						

				## display successful swipe and machine selected	
				print "User is authorized for machine:  " + selected_machine_id



			## Now manage each of the machine states
			for machine in machine_list:
			
				## pass in scanned user (if any) and which machine was selected
				## to main state handling routines for various machines/plugs
				machine.manageState(scanned_username, selected_machine_id)

                except (KeyboardInterrupt):
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
	                
			print "Creating machine ID: %s\nPaired With Plug: %s\nPlug IP Address %s\n" % \
				(machine['machine_description'],machine['plug_description'],machine['ip_address'])
			try:
                		new_machine = Machine.Machine(machine['machine_id'], \
				machine['machine_description'], \
				machine['plug_id'], machine['plug_description'], \
				machine['ip_address'], machine['plug_type'], \
				machine['plug_name'])

				machine_list.append(new_machine)
				MakerPassDatabase.clearMachineUser(new_machine.machine_id)
			except:
				print "Failed to Instantiate machine:  " + machine['machine_description']
				## continue...non-fatal 

	return machine_list

## --------------------------------------------------------
if __name__ == '__main__': main()

