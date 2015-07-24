#!/usr/bin/python

import sqlite3 as lite
import sys
import os.path 


## add main makerpass dir to path for import search
sys.path.insert(0, '/home/pi/makerpass/MakerPass')
from MachineStates import MachineStates

database = '/home/pi/makerpass/MakerPass/database/makerpass_database.db'

## -------------------------------------------------------
## return machine data with current user
def getMachineUsageData():

	con = None

	try:
    		con = lite.connect(database)
   
    		con.row_factory = lite.Row 
    		cur = con.cursor()    

    		# select machine usage data into temp table.  This query is selecting data as a union of 
		# machines with active/running users and machines without.  This is because the active user machines
		# calculate the active running time for the user, whereas the ones with no active user just
		# use null as the running time....note: can this be re-written as just a case statement for 
		# the running_time rather than a union?  Note 2:  Currently this query returns any machine with
		# an associated plug and an associated user in user_machine_allocation_rec....this is as 
		# opposed to only selecting machines that this controller is master for...a calculated step, 
		# but there is an argument for not doing that way...we erred on the side of too much data.  
		sql = """
create temporary table a as select distinct machine_rec.machine_id, machine_description, parent_machine_id, current_state, current_user, last_scan, cast(((julianday(datetime('now', 'localtime')) - julianday(last_scan)) * 1440) as integer) running_time 
from machine_rec
join smartplug_rec on (smartplug_rec.plug_id = machine_rec.plug_id)
left join user_machine_allocation_rec on (user_machine_allocation_rec.machine_id = machine_rec.machine_id)
where current_user=username

union

select distinct machine_rec.machine_id, machine_description, parent_machine_id, current_state, current_user, null last_scan, null running_time
from machine_rec
join smartplug_rec on (smartplug_rec.plug_id = machine_rec.plug_id)
left join user_machine_allocation_rec on (user_machine_allocation_rec.machine_id = machine_rec.machine_id)
where (current_user = '' or current_user = 'none')

;
"""
    		cur.execute(sql) 

		sql = "select distinct * from a;"
		cur.execute(sql)

		rows = cur.fetchall()
		return rows

	except lite.Error, e:
    		print "Error %s:" % e.args[0]
    		sys.exit(1)
    
	finally:
    		if con: con.close()

## ----------------------------------------------------------

## get mapping between machines and scanners
def getMachineScannerData(MY_MASTER_CONTROLLER_ID):

        con = None

        try:
                con = lite.connect(database)

                con.row_factory = lite.Row
                cur = con.cursor()

                # select data from a table
                sql = """
		select * 
		from 
		machine_rec 
		join machine_scanner_table on (machine_scanner_table.machine_id = machine_rec.machine_id) 
		join smartplug_rec on (machine_rec.plug_id = smartplug_rec.plug_id) 
		where parent_machine_id = '""" + MY_MASTER_CONTROLLER_ID + """';"""
                
		cur.execute(sql)

                rows = cur.fetchall()
                return rows

        except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)

        finally:
                if con: con.close()


## ----------------------------------------------------------

def printSystemStatus():

	## check if makerpass is running
	if (os.path.exists("/home/pi/makerpass/MakerPass/process_online")):
        	status = "<font color='green'>ONLINE</font>"
	else:
        	status = "<font color='red'>OFFLINE</font>"

	return "The system is:  " + status + "<br><br>"

## ----------------------------------------------------------

def printMachineRecTable():
        rows = getMachineUsageData()

        response = '<table id="machine_table"  class="display"  border="4" >'
	response += "<tr><th>Machine</th><th>Current User</th><th>Last Scan</th><th>Machine State</th><th>Running Time (min)</th></tr>" 
        for row in rows:

		running_time = row['running_time']
		if (row['current_state'] != MachineStates.toString(MachineStates.STATE_ALL_ON)):
			running_time = 0

		response += "<tr>"
                response += "<td>" + row['machine_description'] + "</td><td>" + str(row['current_user']) +  "</td><td>" + str(row['last_scan']) + "</td><td>" + row['current_state'] + "</td><td>" + str(running_time) + "</td>"
		response += "</tr>"
	response += "</table>"

        return response
## ----------------------------------------------------------

def printMachineSelectDropdown(MY_MASTER_CONTROLLER_ID):

        rows = getMachineScannerData(MY_MASTER_CONTROLLER_ID)
        response = '<select name="scanner_id">'
        for row in rows:
                response += "<option value = \"" + row['scanner_id'] + "\" >" + str(row['machine_description']) +  "</option>" 
        response += "</select>"

        return response

## ----------------------------------------------------------

def loginUser(machine_id, user_id):

	pipe = open("/home/pi/makerpass/MakerPass/pipe_scan", "w")
	pipe.write(str(machine_id) + "|" + str(user_id) + "\n")
	pipe.close()

	return ""


## ----------------------------------------------------------

def headsUpDisplay():
	
	response = printMachineRecTable() 
	
	return response

if __name__ == '__main__':
	print headsUpDisplay()
 
