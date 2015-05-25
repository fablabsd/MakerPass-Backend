#!/usr/bin/python

import os
import sys
import time
import SharedMem
import Machine
import PLNU_IDCardSwipe
import MakerPassDatabase

from multiprocessing import Process


## -------global variables---------------------------------

## set controller ID for this controller
MY_MASTER_CONTROLLER_ID = os.environ["MY_MASTER_CONTROLLER_ID"]


## --------------------------------------------------------
## -------- main ------------------------------------------
## --------------------------------------------------------

def main():

	## Set up shared mem, default scan_id and machine_id
	print "Creating Shared mem" 
	shared_mem = SharedMem.Mem()

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
        Process(target=PLNU_IDCardSwipe.main, args=(shared_mem,MY_MASTER_CONTROLLER_ID)).start()
	
	## main loop
	print "Entering main processing loop..."
	while (True):	

		try:

			scanned_user = ""
	
			## retrieve scan/swipe info if a scan has been made
			scan_id, selected_machine_id = shared_mem.get_shared_mem_values()

			## handle a valid scan
			if (scan_id != ""):

				## first reset the shared mem, to minimize potential 
				## for failed scans from other machines
				shared_mem.set_shared_mem_values('','')

				## TBD:  Check existence of user
				##       and has alloted time
				
				## TBD:  set scanned_user = database.getuserfromscanid(scan_id)
				## TBD:  database.setlastscan(scanned_user)
				scanned_user = "chrisanderson"

				## TBD:  if not valid id -- error
				## TBD:  if no alloted time left for user -- error
				## TBD:   potentially need to get machine_id from a mapping table of 
				## scanner ids (specific to hardware, e.g. SSID) to machine_ids if we are not able
				## to load machine_ids directly onto scanners

				## display successful swipe and machine selected	
				print scan_id
				print selected_machine_id

			## TBD:  don't forget to prevent same user from logging into multiple machines
			## this function checks user=machine.user for all machines that do no match 
			## selected_machine_id (and not counting blank users)
			#if (isUserAlreadyUsingAnotherMachine()): 
				#print "You can't do that you're already logged into another machine"
				#continue

			## Now manage each of the machine states
			for machine in machine_list:
			
				## pass in scanned user (if any) and which machine was selected
				## to main state handling routines for various machines/plugs
				machine.manageState(scanned_user, selected_machine_id)

                except (KeyboardInterrupt):
                        break

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
	                
			print "Creating machine ID: %s" % machine['description']
                	new_machine = Machine.Machine(machine['machine_id'], machine['plug_id'])
			machine_list.append(new_machine)

	return machine_list

## --------------------------------------------------------
if __name__ == '__main__': main()

