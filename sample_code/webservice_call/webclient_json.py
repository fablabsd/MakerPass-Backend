#!/usr/bin/python


import urllib2
import sys
import json
from pprint import pprint

## ------- main------------------------------------------------------

## verify program arguments
if (len(sys.argv) < 2):
        print "\nUsage:  python webclient_json.py <url> \n\n"
        sys.exit(0)

responsedata = ""

try:
	url = urllib2.Request(sys.argv[1])
	responsedata = urllib2.urlopen(url).read()
except urllib2.HTTPError, e:
	print "HTTP error: %d" % e.code
except urllib2.URLError, e:
	print "Network error: %s" % e.reason.args[1]

#print responsedata

## now parse json output from url
try:
	#with open('sample.json') as data_file:    
		#data = json.load(data_file)
	data = json.loads(responsedata)
	pprint(data)
except:
	print "Exception parsing JSON data"
	sys.exit(1)


print
print
#print "User ID: " + str(data["userId"]) 
#print "Title:  " + data["title"]
for key in data:
    print "data[" + str(key) + "] = " + str(data[key])
