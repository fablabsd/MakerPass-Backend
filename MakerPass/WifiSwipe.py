#!/usr/bin/python


##
## WifiSwipe.py -- Read a scan from a pipe, authorize it, then send a response
## this works just like PipeSwipe, but sends a response back through the pipe
##
import sys

from MakerPassLogger import WifiSwipe_logger as logger
from RegisterScan import registerScan

## ------- main------------------------------------------------------

def main(shared_mem, null_param):
 
	## before entering main loop, clear out the pipe
	## to ensure any orphaned logins aren't picked up
	## at initialization time
	#logger.debug("Clearing out wifi_scan pipe")
        #pipe = open("/home/pi/makerpass/MakerPass/wifi_scan", "r")
        #old_scan = pipe.read().rstrip()
        #pipe.close()

	while (True): 

		try:

			## get the swipe from the pipe = scanner_id + username
        		pipe = open("/home/pi/makerpass/MakerPass/wifi_scan", "r")
			scan = pipe.read().rstrip()
			pipe.close()
			
			logger.debug( scan + "\n")
			
			## strip out machine id and username
			scanner_id, scan_id, client_ip = scan.split("|")

			logger.debug( "scanned scanner_id from wifi pipe:  " + scanner_id)
			logger.debug( "scanned scan_id from wifi pipe:  " + scan_id)
			logger.debug( "scanned client_ip from wifi pipe:  " + client_ip)

			try:

        			## If the submitted user+scanner are valid,
        			## submit them via the pipe to makerpass
        			if (scanner_id and scan_id):
					response = "0"
                			ret_val, scanned_username, selected_machine_id = registerScan(scan_id, scanner_id)
                			if (ret_val == 0):
						## register complete scan by updating synchronized variables
						## note we are shoehorning username and machine_id in here rather
						## than scan_id and scanner_id since we validated them already 	
						shared_mem.set_shared_mem_values(scanned_username, selected_machine_id, client_ip, "False")
                        			response = "1"
					sendResponse(response)

			except Exception as e:
        			logger.debug("Error %s:" % e.message)
        			sendResponse("0")


					
	
		except (KeyboardInterrupt):
			break

def sendResponse(response):

        pipe = open("/home/pi/makerpass/MakerPass/wifi_response", "w")
        pipe.write(str(response) + "\n" )
        pipe.close()
