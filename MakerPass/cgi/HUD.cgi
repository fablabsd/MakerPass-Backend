#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import MakerPassWebClient

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

## get which cluster controller this is from config
config_fd = open("/home/pi/makerpass/MakerPass/cluster_controller.config", "r")
MY_MASTER_CONTROLLER_ID = config_fd.read().rstrip()
config_fd.close()

## headers
print "Content-type: text/html\n\n";
#print "<html><meta http-equiv=\"refresh\" content=\"9\" ><body>"
print "<html>"
print '<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">'
print '<META HTTP-EQUIV="PRAGMA" CONTENT="NO-CACHE">'
print """
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
   <script>
 function autoRefresh_div()
 {
      $("#machine_table").load("machine_table.cgi"); // a function which will load data from other file after x seconds
  }

  autoRefresh_div(); 
  setInterval('autoRefresh_div()', 5000); // refresh div after 5 secs
            </script>
"""
print "<body>"


## show heads-up display
print "<br><br>"
print "<h3>Machine Status:</h3><br>"
print "<div id=\"machine_table\">"
#print MakerPassWebClient.printMachineRecTable()
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


print '<form action="/cgi-bin/HUD.cgi" method="post">'
print "<br>"
print "<h3>Manual Login/Logout:</h3><br>"
#print 'Machine ID: <input type="text" name="scanner_id"><br />'

print MakerPassWebClient.printMachineSelectDropdown(MY_MASTER_CONTROLLER_ID)
print "&nbsp&nbsp&nbsp"
print 'ID Number: <input type="text" name="user_id" />'

print '<input type="submit" value="Submit" />'
print '</form>'


##  footers
print "</body>"
print "</html>"
