#!/usr/bin/python

import MakerPassDatabase

rows = MakerPassDatabase.getMachineUsers()
print rows        
for row in rows:
	print  row['username'] + "\n"

