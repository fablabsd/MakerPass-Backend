#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import MakerPassWebClient

print "Content-type: text/html\n\n";

print "<html><body>"
print MakerPassWebClient.printMachineRecTable()
print "</body></html>"


