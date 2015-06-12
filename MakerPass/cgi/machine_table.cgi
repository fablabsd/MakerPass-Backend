#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import MakerPassWebClient

print "Content-type: text/html\n\n";

print "<html><body>"
print """
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 15px;
}
</style>"""

print MakerPassWebClient.printMachineRecTable()
print "</body></html>"


