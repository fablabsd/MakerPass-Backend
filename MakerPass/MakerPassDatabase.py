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

if __name__ == '__main__': 

	rows = getMachineRecords()
        for row in rows:
		print "keys = ",row.keys()
		print row['machine_id'], row['parent_machine_id']
     		#for col in row:
                        #print col + " ",
                        #print
	#for key in rows[0]:
	#print rows
		#print "key = ",key
