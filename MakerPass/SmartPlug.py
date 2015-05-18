#!/usr/bin/python



class SmartPlugTypes:
        ## enumerated smartplug types
        WEMO_INSIGHT_SMARTPLUG = 0
        XYZ_MANUFACTURER_ETHERNET_MULTIPLUG = 1
        OTHER_XYZ_MAKE_SMARTPLUG = 2

class SmartPlug(object):
        
	def __init__(self, plug_id, description, ip_address, type):
                self.plug_id = plug_id
                self.description = description
                self.ip_address = ip_address
		self.type = type
		#plug_type = SmartPlugTypes.WHATEVS	

