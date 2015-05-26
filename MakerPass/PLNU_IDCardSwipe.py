#!/usr/bin/python


##
## PLNU_IDCardSwipe.py -- Read a string from a rawHID device in /dev and print the ascii converted contents
##
import sys

## define number of bytes to read into buffer - 
## Note:  This value is set low as we will loop through
## reading this many bytes from the device buffer until 
## we have everything we need (up to the stop byte)
MAX_BUF_SIZE = 10

## define the byte that ends a complete read
STOP_BYTE = 88

## This is a mapping of the input codes to numerals
keymap = {39: 0, 30 : 1, 31 : 2,32 : 3,33 : 4,34 : 5,35 : 6,36 : 7,37 : 8,38 : 9}; 

## holds the raw input values, converted from ascii -- we will
## only use the values from this list that are valuable data
rawdata = [];


## ------- main------------------------------------------------------

def main(shared_mem, machine_id):
  

	MY_MACHINE_ID = machine_id
 
	## first obtain which /dev device we will be reading from
	config_fd = open("magstripe_scan_usb_port.config", "r+")
	device_name = config_fd.read().rstrip()
	config_fd.close()

	## if device name not found, we have no mag stripe attached
	## so just exit
	if (device_name.rstrip() == ""):
		print "No PLNU mag stripe found as STMMicroelectronics Keyboard"
		sys.exit(0)

	
	## Open the device for reading 
	print "Opening STMMicroelectronics Keyboard device for PLNU magstripe swipe"
	fd = open("/dev/" + device_name, "r+")
	print "Device name: ", fd.name

	while(True): 

		try:

			## Read from device 
			strbuf = fd.read(MAX_BUF_SIZE);

			## Loop through each character, and if it's > 0 
			## (i.e not noise) save it's int value to an ID string
			for character in strbuf:

				## skip if noise
				intval = ord(character)
				if (intval == 0): continue  ## skip noise
				
				## append swipe char to list
				rawdata.append(intval)

				## save value if we reached end of swipe
				if (intval == STOP_BYTE):   
					#print "\n"
					## strip out only the values from our input string that we care about
					outstring = str(keymap[rawdata[10]]) + str(keymap[rawdata[11]]) + \
					str(keymap[rawdata[12]]) + str(keymap[rawdata[13]]) +  \
					str(keymap[rawdata[14]]) + str(keymap[rawdata[15]])
					
					## register complete scan by updating synchronized variables 	
					shared_mem.set_shared_mem_values(outstring, MY_MACHINE_ID)

	
		except (KeyboardInterrupt):
			break

	## close down device
	fd.close()


