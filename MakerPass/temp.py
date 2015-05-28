
import sys

while True:

	try:

		fd = open("machine_on.txt","r+")
		if (fd != None):  
			print "yes"
			fd.close()

	except IOError:
		print "no"



