#!/usr/bin/python

import sqlite3 as lite
import sys


## return all the values as row data from machine_rec
def getMachineRecords():

	con = None

	try:
    		con = lite.connect('database/makerpass_database.db')
   
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
                con = lite.connect('database/makerpass_database.db')

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
                con = lite.connect('database/makerpass_database.db')

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
                con = lite.connect('database/makerpass_database.db')

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

## ----------------------------------------------------------
def updateUserScanRecords(username, machine_id):

        con = None

        try:
                con = lite.connect('database/makerpass_database.db')

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

if __name__ == '__main__': 

	rows = getMachineRecords()
        for row in rows:
		#print "keys = ",row.keys()
		print row['machine_id'], row['parent_machine_id']
     		#for col in row:
                        #print col + " ",
                        #print
	#for key in rows[0]:
	#print rows
		#print "key = ",key

	updateUserScanRecords("testuser","FABLAB_CNC1")

	row = getMachineId("PLNU_MAG_SWIPE")
	print row['machine_id']

	row = getUserMachineInfo("testuser", "FABLAB_CNC1") 
	print row['last_scan']
