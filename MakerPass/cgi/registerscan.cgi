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
client_ip = os.environ["REMOTE_ADDR"]

#print "Content-Type: application/json";
print "Content-type: text/html\n\n";
print "<html>"
print "<body>"

try: 

	## If the submitted user+scanner are valid, 
	## submit them via the pipe to makerpass
	if (scanner_id and user_id):
		ret_val, dummy1, dummy2 = registerScan(user_id, scanner_id) 
		if (ret_val == 0):
			MakerPassWebClient.loginUser(scanner_id, user_id, client_ip)
			print "{1}"

	print "{0}"

except Exception as e:
	print "except"
	print "{0}"
	print "Error %s:" % e.message
print "</body>"
print "</head>"
