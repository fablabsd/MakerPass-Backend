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
    		cur.execute('select * from machine_rec;') 
    		
		rows = cur.fetchall()
		return rows

	except lite.Error, e:
    		print "Error %s:" % e.args[0]
    		sys.exit(1)
    
	finally:
    		if con: con.close()

## ----------------------------------------------------------
## return row data for a given smartplug_rec
def getSmartPlugData(plug_id):

        con = None

        try:
                con = lite.connect('database/makerpass_database.db')

                con.row_factory = lite.Row
                cur = con.cursor()

                # select data from a table
                cur.execute('select distinct * from smartplug_rec where plug_id = "' + plug_id + '"')

                rowdata = cur.fetchall()
                return rowdata

        except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)

        finally:
                if con: con.close()

if __name__ == '__main__': 

	rows = getMachineRecords()
        for row in rows:
		print row['machine_id'], row['parent_machine_id']
     		#for col in row:
                        #print col + " ",
                        #print
	rowdata = getSmartPlugData('WEMO_LASER1')
        for row in rowdata:
                print row['plug_id'], row['description'], row['ip_address'], row['statemap_type']
                #for col in row:
                        #print col + " ",
                        #print

