#!/usr/bin/python

##
## readSTMKeyboardHID.py -- Read a string from a rawHID device in /dev and print the ascii converted contents
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

## hold the final dataa
ID = -1

## ------- main------------------------------------------------------

## verify program arguments
if (len(sys.argv) < 2): 
	print "\nUsage:  python readSTMKeyboardHID.py <device from /dev>\n\n"
	sys.exit(0)
    
## Open the device for reading 
fd = open(sys.argv[1], "r+")
#print "Name of the file: ", fd.name

need_break = False 
while(True): 

	try:

		## Read from device 
		strbuf = fd.read(MAX_BUF_SIZE);

		## Loop through each character, and if it's > 0 
		## (i.e not noise) save it's int value to an ID string
		for character in strbuf:

			intval = ord(character)
			if (intval == 0): continue  ## skip noise

			#sys.stdout.write("%i " % intval)
			print intval,
			rawdata.append(intval)
			if (intval == STOP_BYTE):   
				print "\n"
				## strip out only the values from our input string that we care about
				outstring = str(keymap[rawdata[10]]) + str(keymap[rawdata[11]]) + \
				str(keymap[rawdata[12]]) + str(keymap[rawdata[13]]) +  \
				str(keymap[rawdata[14]]) + str(keymap[rawdata[15]])
				ID = int(outstring)
				print ID


		## flush output			
		sys.stdout.flush() 

	except (KeyboardInterrupt):
		break

## We won't get here, but for solidarity..
fd.close()


