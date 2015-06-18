#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import MakerPassWebClient

print "Content-type: text/html\n\n";

print "<html><body>"
print """
<style>


</style>"""
print "<font color='red'>" 

feedback_file = open("/home/pi/makerpass/MakerPass/cgi/user_feedback.txt", "r+")
print feedback_file.read()
feedback_file.close()

print "</font>"
print "</body></html>"


