#!/usr/bin/python

## defines
header_indexes = {'user_id': -1, 'username': -1, 'firstname': -1, 'lastname': -1, 'total_time_allocated': -1, 'time_allocated':-1, 'machine_id':-1} 

## open input csv file
fd = open("/home/pi/makerpass/MakerPass/database/user_import/user_import.csv", "r+")
split_header = fd.readline().rstrip('\n').split(",")

#print split_header

## associate the header column with it's index in the row
## so we don't have to worry about ordering of the columns
for i in range(len(split_header)):
	for key in header_indexes:
		if (key == split_header[i]):
			header_indexes[key] = i

#for key in header_indexes:
	#print key + ": " + str(header_indexes[key])


## first inactivate all entries of user_machine_allocation_rec
print "update user_machine_allocation_rec set inactive_date = date('now');"

## same for user_rec
print "update user_rec set inactive_date = date('now');"

## activate and insert those from input file
for line in fd:
	split_line = line.rstrip('\n').split(",")
	#print split_line
	#print split_line[header_indexes['user_id']]
	user_id = split_line[header_indexes['user_id']]
	username = split_line[header_indexes['username']]
	firstname = split_line[header_indexes['firstname']]
	lastname = split_line[header_indexes['lastname']]
	time_allocated = split_line[header_indexes['time_allocated']]
	total_time_allocated = split_line[header_indexes['total_time_allocated']]
	machine_id = split_line[header_indexes['machine_id']]

	## first do an insert of all rows, ignoring those that exist
	print """
insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select '""" + username + """', '""" + machine_id + """', """ + time_allocated + """, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'""" + username + """' and machine_id = '""" + machine_id + """'); """

	## same for user_rec
	print """
insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select """ + user_id + """, '""" + username + """', '""" + firstname + """', '""" + lastname + """', """ + total_time_allocated + """, date('now') 
where not exists(select username from user_rec where username=
'""" + username + """' ); """

	## now go back and update those that already exist as being active
	print """
update user_machine_allocation_rec set inactive_date = null where username= 
'""" + username + """' and machine_id = '""" + machine_id + """'; """ 

	## same for user_rec again
	print """
update user_rec set inactive_date = null where username= 
'""" + username + """' ; """ 

fd.close()

