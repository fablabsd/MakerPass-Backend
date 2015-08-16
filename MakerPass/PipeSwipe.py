#!/usr/bin/python


##
## pipe_swipe.py -- Read a swipe from a pipe (no rhyming please)
##
import sys

from MakerPassLogger import PipeSwipe_logger as logger

## ------- main------------------------------------------------------

def main(shared_mem, null_param):
 
	
	while (True): 

		try:

			## get the swipe from the pipe = scanner_id + username
			pipe = open("pipe_scan", "r")
			scan = pipe.read().rstrip()
			pipe.close()
			
			logger.debug( scan + "\n")
			
			## strip out machine id and username
			scanner_id, scan_id, client_ip = scan.split("|")
			#scanner_id = "PLNU_MAG_SWIPE"
		 	#scan_id = "439003"
			

			logger.debug( "scanned scanner_id from pipe:  " + scanner_id)
			logger.debug( "scanned scan_id from pipe:  " + scan_id)
			logger.debug( "scanned client_ip from pipe:  " + client_ip)
					
			## register complete scan by updating synchronized variables 	
			shared_mem.set_shared_mem_values(scan_id, scanner_id, client_ip, "True")
					
	
		except (KeyboardInterrupt):
			break

