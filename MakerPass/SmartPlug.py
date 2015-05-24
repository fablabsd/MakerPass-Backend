#!/usr/bin/python


class SmartPlug(object):
        
	def __init__(self, plug_id, description, ip_address, statemap_type):
                self.plug_id = plug_id
                self.description = description
                self.ip_address = ip_address
		self.statemap_type = statemap_type

