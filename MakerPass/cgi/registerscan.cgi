#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import MakerPassWebClient
import subprocess
import os
import sys

## add base makerpass path to path before importing
## register scan lib
sys.path.insert(0, '/home/pi/makerpass/MakerPass')
from RegisterScan import registerScan

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
scanner_id = form.getvalue('scanner_id')
user_id  = form.getvalue('user_id')
use_json  = form.getvalue('use_json')
client_ip = os.environ["REMOTE_ADDR"]

#print "Content-Type: application/json\n\n"
json_header = "Content-Type: application/json\n\n"
html_header =  "Content-type: text/html\n\n<html><body>"
html_footer =  "</body></html>"

try: 

	## If the submitted user+scanner are valid, 
	## submit them via the pipe to makerpass
	if (scanner_id and user_id):

		## send our scan through the pipe
	        pipe = open("/home/pi/makerpass/MakerPass/wifi_scan", "w")
	        pipe.write(str(scanner_id) + "|" + str(user_id) + "|" + str(client_ip) + "\n")
        	pipe.close()

		## now read the response from the pipe
		pipe = open("/home/pi/makerpass/MakerPass/wifi_response", "r")
		response = pipe.read().rstrip()
		pipe.close()

		if (use_json and use_json == "1"): 
			print json_header + "{response:" + str(response) + "}"
		else:
			print html_header + str(response)  + html_footer
			

except Exception as e:
	print  "Exception %s:" % e.message

