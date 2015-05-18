#!/usr/bin/python

import time
from multiprocessing import Process, Value, Array, Lock


## This is not a shared object even though it may seem like one --
## It's just a bunch of individual shared variables wrapped in a class
## so we have a convenient namespace for shared mem ...It should be a 
## shared object but python shared memory sucks

class Mem(object):
    def __init__(self):

	## Yes...creating a shared memory variable for a string is an 
	## array of characters called "Array" the multiprocessing library
	## ...not exactly a well thought out naming scheme nor implementation
	## as I must now create a "max" number of characters in order to prevent
	## size errors
        self.scan_id = Array('c', ' ' * 128)
        self.selected_machine_id = Array('c', ' ' * 128)
        self.lock = Lock()

    def set_shared_mem_values(self,scan_id_value, selected_machine_id_value):
	with self.lock:
		self.scan_id.value = scan_id_value
		self.selected_machine_id.value = selected_machine_id_value

    def get_shared_mem_values(self):
	with self.lock:
		return (self.scan_id.value, self.selected_machine_id.value) 






