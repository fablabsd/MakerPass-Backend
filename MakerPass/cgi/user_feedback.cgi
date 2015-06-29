#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import MakerPassWebClient

print "Content-type: text/html\n\n";

print "<html><body>"
print """
<style>


</style>"""
print "<h1><font color='red'>" 

## read in the feedback message
feedback_file = open("/home/pi/makerpass/MakerPass/cgi/user_feedback.txt", "r+")
feedback_message = feedback_file.read()
feedback_file.flush()

## we have the message, now clear out the file
feedback_file.seek(0,0)
feedback_file.truncate()
feedback_file.close()

print feedback_message

## we have the message, now clear out the file
#feedback_file2 = open("/home/pi/makerpass/MakerPass/cgi/user_feedback.txt", "w")
#feedback_file2.write("")
#feedback_file2.close()


print "</font></h1>"
print "</body></html>"


