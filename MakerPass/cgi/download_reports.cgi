#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import MakerPassWebClient

print "Content-type: text/html\n\n";
#print "Content-Disposition: attachment; filename=\"temp.csv\""
print "<html><body>"
print "<h3>Download Reports</h3>"
print "<br>"
print "<br>"
print "<a href=\"/reports/machine_usage_per_person.csv\" download >machine_usage_per_person.csv </a>" 

print "</body></html>"


