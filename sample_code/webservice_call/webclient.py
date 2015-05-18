#!/usr/bin/python


import urllib2
import sys
import xml.dom.minidom

from xml.dom.minidom import parse, parseString

## ------- main------------------------------------------------------

## verify program arguments
if (len(sys.argv) < 2):
        print "\nUsage:  python webclient.py <url> \n\n"
        sys.exit(0)

try:
	url = sys.argv[1]
	responsedata = urllib2.urlopen(url).read()
except urllib2.HTTPError, e:
	print "HTTP error: %d" % e.code
except urllib2.URLError, e:
	print "Network error: %s" % e.reason.args[1]

#print responsedata



# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parseString(responsedata)
collection = DOMTree.documentElement
if collection.hasAttribute("xmlns:xlink"):
   print "Root element attribute : %s" % collection.getAttribute("xmlns:xlink")

# Get all the resources in the collection
invoice = collection.getElementsByTagName("INVOICEList")[0]
#print "Invoice: %s" % invoice.data
#print invoice.firstChild.data
print "Invoice: %s" % invoice.childNodes[0].data

'''
# Print detail 
for invoice in invoices:
   print "***** Invoice *****"
   invoice = resource.getElementsByTagName('INVOICEList')[0]
   print "Invoice: %s" % invoice.childNodes[0].data

'''
