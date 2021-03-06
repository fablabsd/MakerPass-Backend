#!/usr/bin/python

import sqlite3 as lite
import sys

database = '/home/pi/makerpass/MakerPass/database/makerpass_database.db'

## return all the values as row data from machine_rec
def getMachineRecords():

	con = None

	try:
    		con = lite.connect(database)
   
    		con.row_factory = lite.Row 
    		cur = con.cursor()    

    		# select data from a table 
    		cur.execute('select * from machine_rec join smartplug_rec on (smartplug_rec.plug_id = machine_rec.plug_id);') 
		rows = cur.fetchall()
		return rows

	except lite.Error, e:
    		print "Error %s:" % e.args[0]
    		sys.exit(1)
    
	finally:
    		if con: con.close()

## ----------------------------------------------------------
def getUserInfo(scan_id):

        con = None

        try:
                con = lite.connect(database)

                con.row_factory = lite.Row
                cur = con.cursor()

                # select data from a table
                sql = 'select * from user_rec where user_id = ' + scan_id + ';'
                cur.execute(sql)
                rows = cur.fetchall()

                ## return first, and only row
                for row in rows:
                        return row

                return None


        except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)

        finally:
                if con: con.close()

## ----------------------------------------------------------
def getMachineId(scanner_id):

        con = None

        try:
                con = lite.connect(database)

                con.row_factory = lite.Row
                cur = con.cursor()

                # select data from a table
		sql = "select machine_id from machine_scanner_table where scanner_id = '" + scanner_id + "';"
                cur.execute(sql)
                rows = cur.fetchall()

                ## return first, and only row
                for row in rows:
                        return row

                return None


        except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)

        finally:
                if con: con.close()

## ----------------------------------------------------------
def getUserMachineInfo(username, machine_id):

        con = None

        try:
                con = lite.connect(database)

                con.row_factory = lite.Row
                cur = con.cursor()

                # select data from a table
                sql = """ select * from user_machine_allocation_rec where username = '"""  + username + """'
			 and machine_id = '""" + machine_id + """';"""


                cur.execute(sql)
                rows = cur.fetchall()
		
		## return first, and only row 
		for row in rows:
			return row
                
		return None

        except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)

        finally:
                if con: con.close()


## ----------------------------------------------------------
def updateUserScanRecords(username, machine_id):

        con = None

        try:
                con = lite.connect(database)

                con.row_factory = lite.Row
                cur = con.cursor()

                # first insert a scan record
		sql = "insert into user_machine_scan_rec (username, machine_id, scan_timestamp) values ('" + username + "', '" + machine_id + "', (DATETIME('now')));"

                cur.execute(sql)

		## update the machine-specific last scan
		sql = "update user_machine_allocation_rec set last_scan = (DATETIME('now')) where username = '" + username + "' and machine_id = '" + machine_id + "';"
		cur.execute(sql)

		## update the user-specific last scan
		sql = "update user_rec set last_scan = (DATETIME('now')) where username = '" + username + "';"
		cur.execute(sql)

		con.commit()
                return None

        except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)

        finally:
                if con: con.close()

## ----------------------------------------------------------
def recordTimeUsed(username, machine_id):

        con = None

        try:
                con = lite.connect(database)

                con.row_factory = lite.Row
                cur = con.cursor()

                ## update user_machine_allocation_rec by setting time_logged to now minus last scan time
		## julinaday() is used, but note this still has time info after decimal point so we just
		## cast to minutes by multiplying by number of minutes in a day 
                sql = "update user_machine_allocation_rec set time_logged= cast((time_logged + (julianday(datetime('now')) - julianday(last_scan)) * 1440) as integer) where username='" + username + "' and machine_id='" + machine_id + "';"
                cur.execute(sql)

                ## update the user-specific time_logged - same as above but for user_rec
                sql = "update user_rec set total_time_logged= cast((total_time_logged + (julianday(datetime('now')) - julianday(last_scan)) * 1440) as integer) where username='" + username + "';"
                cur.execute(sql)

                con.commit()
                return None

        except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)

        finally:
                if con: con.close()

## ----------------------------------------------------------

def markMachineEffectiveUseTime(username, machine_id):



        try:
                con = lite.connect(database)

                con.row_factory = lite.Row
                cur = con.cursor()


                ## update the machine effective_use_time -- this is the time
		## the machine was turned off (if supported, otherwise this will be the same as 
		## the scan time
                sql = "update user_machine_allocation_rec set last_scan = (DATETIME('now')) where username = '" + username + "' and machine_id = '" + machine_id + "';"
                cur.execute(sql)

                ## update the user-specific last scan
                sql = "update user_rec set last_scan = (DATETIME('now')) where username = '" + username + "';"
                cur.execute(sql)

                con.commit()
                return None

        except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)

        finally:
                if con: con.close()


## ----------------------------------------------------------
def printMachineRecs():
	rows = getMachineRecords()
	response = ""
        for row in rows:
		response += row['machine_id'] + " " +  row['parent_machine_id'] + " " + row['current_user'] + "<br>\n"

	return response


def headsUpDisplay():
	response = "<html><meta http-equiv=\"refresh\" content=\"5\" ><body>"
	response += printMachineRecs() 
	response += "</body></html>"
	
	return response

if __name__ == '__main__':
	print headsUpDisplay()
 
