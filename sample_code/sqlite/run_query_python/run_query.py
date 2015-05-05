#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('machine_config.db')
   
    ## first run a simple query that gets the version 
    #configure result set to be "Row" type which 
    #enables indexing columns by name i.e.
    con.row_factory = lite.Row 
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data                

    # select data from a table and iterate all rows
    cur.execute('select * from machine_config') 
    rows = cur.fetchall()
    # iterate rows
    for row in rows:
	for col in row:
            print col + " ", 
        print 

    # just get a single element from this row
    print
    print row['machine_id']
    

	 
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()

