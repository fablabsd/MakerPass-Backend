#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import MakerPassWebClient
import subprocess

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

## get which cluster controller this is from config
config_fd = open("/home/pi/makerpass/MakerPass/cluster_controller.config", "r")
MY_MASTER_CONTROLLER_ID = config_fd.read().rstrip()
config_fd.close()

## headers
print "Content-type: text/html\n\n";
print "<html>"
print '<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">'
print '<META HTTP-EQUIV="PRAGMA" CONTENT="NO-CACHE">'
print """
    <head>
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.7/css/jquery.dataTables.css">
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script src="https://code.jquery.com/jquery-1.11.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>
   <script>
$(document).ready(function() {
	$('#machine_table').DataTable();
	autoRefresh_div();
} );
   </script>
   <script type="text/javascript">
 function autoRefresh_div()
 {
	// a function which will load data from other file after x seconds
      $("#machine_table_div").load("machine_table.cgi"); 
     
	// show response from makerpass to attempted user login or other issues/info 
	$("#feedback_div").load("user_feedback.cgi"); 
  }

  setInterval('autoRefresh_div()', 15000); // refresh div after 15 secs
            </script>


</head>
"""
print "<body>"

## show heads-up display
print "<h1>Welcome to Makerpass</h1><br><br>"

## print the manual login controls 
print '<form action="/cgi-bin/HUD.cgi" method="post">'
print "<br>"
print "<h3>Manual Login/Logout:</h3><br>"

print MakerPassWebClient.printMachineSelectDropdown(MY_MASTER_CONTROLLER_ID)
print "&nbsp&nbsp&nbsp"
print 'ID Number: <input type="text" name="user_id" />'

print '<input type="submit" value="Submit" />'
print '</form>'
print '<br>'

## print user feedback from submission if applicable
print "<div id=\"feedback_div\">"
print "</div>"

## machine/user table
print "<br><br>"
print "<h3>Machine Status:</h3>"
print "<div id=\"machine_table_div\">"
print "Waiting for data...<br>"
print "</div>"

## refresh button
#print '<button onclick="window.location.href=\'/cgi-bin/HUD.cgi\'">Refresh</button>'

# Get data from fields
scanner_id = form.getvalue('scanner_id')
user_id  = form.getvalue('user_id')

#print "selected scanner_id = " + str(scanner_id) + "<br>"
#print "selected user_id = " + str(user_id)

## if a login was submitted process it
if (scanner_id and user_id):
	print MakerPassWebClient.loginUser(scanner_id, user_id)

print "<br>"

system_load_str =  subprocess.Popen("uptime | cut -d\":\" -f5", shell=True, stdout=subprocess.PIPE).stdout.read()
print "System Load: " + str(system_load_str)

##  footers
print "</body>"
print "</html>"
