#!/usr/bin/python

header_indexes = {'user_id': -1, 'nothing': -1, 'username': -1, 'time_allocated':-1, 'machine_id':-1} 


fd = open("user_machine_allocations.csv", "r+")
split_header = fd.readline().rstrip().split(",")

print split_header

## associate the header column with it's index in the row
## so we don't have to worry about ordering of the columns
for i in range(len(split_header)):
	for key in header_indexes:
		if (key == split_header[i]):
			header_indexes[key] = i

#for key in header_indexes:
	#print key + ": " + str(header_indexes[key])

for line in fd:
	split_line = line.rstrip().split(",")
	#print split_line[header_indexes['user_id']]
	user_id = split_line[header_indexes['user_id']]
	username = split_line[header_indexes['username']]
	time_allocated = split_line[header_indexes['time_allocated']]
	machine_id = split_line[header_indexes['machine_id']]
	print """
	insert into user_machine_allocation_rec (username, machine_id, time_allocated) values (
	'""" + username + """', '""" + machine_id + """', """ + time_allocated + """) """
fd.close()

