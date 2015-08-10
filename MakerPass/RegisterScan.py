#!/usr/bin/python

import os
import sys
import time
import SharedMem
import logging
import MakerPassDatabase
import MakerPassLogger

from datetime import datetime
from MakerPassLogger import RegisterScan_logger as logger
from MachineStates import MachineStates

		
## --------------------------------------------------------
## Read and validate a scan input 

def registerScan(scan_id, scanner_id):

	scanned_username = ""
	selected_machine_id  = ""

	## handle a valid scan
	if (scan_id != ""):
		logger.debug( "scan_id = " + scan_id)
		logger.debug( "scanner_id = " + scanner_id)

		##  get machine_id from a mapping table of scanner IDs 
		## i.e. map scanning device to machine being scanned to
		selected_machine_id_data = MakerPassDatabase.getMachineId(scanner_id)
		if (selected_machine_id_data == None):
			logger.debug( "Unable to associate a machine with this scanner:  " + scanner_id)
			logUserFeedback( "Unable to associate a machine with this scanner:  " + scanner_id)
			return -1, scanned_username, selected_machine_id

		## found machine id
		selected_machine_id = selected_machine_id_data['machine_id']
	
		## Get the user associated with this scan id
		userinfo = MakerPassDatabase.getUserInfo(scan_id)
		if (userinfo == None):
			logger.debug( "No User found with scan_id = " + str(scan_id))
			logUserFeedback( "No User found with scan_id = " + str(scan_id))
			MakerPassDatabase.setLastMessage( "No User found with scan_id = " + str(scan_id), selected_machine_id)
			return -1, scanned_username, selected_machine_id
		
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
			return -1, scanned_username, selected_machine_id
		
		## If no alloted time left for user (total from user_rec) -- error
		if (userinfo['total_time_logged'] >= userinfo['total_time_allocated']):
			logger.debug( "The given user (%s)" % scanned_username)
			logger.debug( " has exceeded the total alloted to them")
			logger.debug( " for all machines.  Please ensure user record is up to date")
			logUserFeedback("User " +  userinfo['firstname'] + " " + userinfo['lastname']  + " Exceeded total time allotment - see administrator for details")
			MakerPassDatabase.setLastMessage( "Total allotted time exceeded for: " + scanned_username, selected_machine_id)
			return -1, scanned_username, selected_machine_id
	
		
		logger.debug( "Time Allocated for " + selected_machine_id + " = " + str(usermachineinfo['time_allocated']))
		logger.debug( "Time Logged for " + selected_machine_id + " = " + str(usermachineinfo['time_logged']))

		logger.debug("here1")
		## If no alloted time left for user on THIS machine 
		## (from user_machine_allocation_rec) -- error
		if (usermachineinfo['time_logged'] >= usermachineinfo['time_allocated']):
			logger.debug( "The given user (%s)" % scanned_username)
			logger.debug( " has no more time left on the scanned machine (%s)" % selected_machine_id)
			logUserFeedback("User " +  userinfo['firstname'] + " " + userinfo['lastname']  + " Exceeded time allotment on the given machine - see administrator for details")
			MakerPassDatabase.setLastMessage( "Allotted time exceeded on this machine for: " + scanned_username, selected_machine_id)
			return -1, scanned_username, selected_machine_id
		logger.debug("here1")
	
		## Prevent same user from logging into multiple machines
		if (isUserAlreadyUsingAMachine(scanned_username, selected_machine_id)): 
			logger.debug( "You can't do that you're already logged into a machine")
			logUserFeedback("User " +  userinfo['firstname'] + " " + userinfo['lastname']  + " is already logged into another machine")
			MakerPassDatabase.setLastMessage( "This user already using another machine: " + scanned_username, selected_machine_id)
  			return -1, scanned_username, selected_machine_id

		logger.debug("here1:" + selected_machine_id)
				
		## Prevent scanning in to a machine that is in the "Unrecognized" state
		machine_state_data = MakerPassDatabase.getMachineState(selected_machine_id)
		if (machine_state_data['current_state'] == "Unrecognized"):
			logger.debug( "Cannot log into a machine that is in the 'Unrecognized' state")
			logUserFeedback(str(selected_machine_id) + " is unavailable/uninitialzed ")
			MakerPassDatabase.setLastMessage("Machine unavailable/uninitialized ", selected_machine_id)
                        return -1, scanned_username, selected_machine_id
		logger.debug("here1")

		## display successful swipe and machine selected	
		logger.debug( "User is authorized for machine:  " + selected_machine_id)
		logUserFeedback("Successfully scanned " +  userinfo['firstname'] + " " + userinfo['lastname']  + " for machine:  " + selected_machine_id)
		logger.debug("here3")
		MakerPassDatabase.setLastMessage( "Authorized Scan: " + scanned_username, selected_machine_id)
		logger.debug("here1")
		
	return 0, scanned_username, selected_machine_id

## --------------------------------------------------------
## this function checks user=machine.user for all machines
## to ensure no attempt is made to log user in multiple machines

def isUserAlreadyUsingAMachine(scanned_username, selected_machine_id):

        ## get users currently using machines from database
        rows = MakerPassDatabase.getMachineRecords()
        for machine in rows:
                if ((machine['machine_id'] != selected_machine_id) and (machine['current_user'] == scanned_username)):
			return True

        return False

## --------------------------------------------------------
## Respond to web client with this feedback

def logUserFeedback(feedbackString):
	logger.debug("here2")
       	feedback_file = open('/home/pi/makerpass/MakerPass/cgi/user_feedback.txt', "w")
        feedback_file.write(feedbackString)
        feedback_file.close()

