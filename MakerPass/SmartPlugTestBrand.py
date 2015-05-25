#!/usr/bin/python

import SmartPlug

class SmartPlugTestBrand(SmartPlug):
        
	def __init__(self, plug_id, description, ip_address):
		SmartPlug.__init__(plug_id, description, ip_address)
		self.switched_on_threshold = 12345  ## need to address what this value should be


        ##  ----- METHODS -------------------------------------
        def enableMachinePlug(self):
                print " SmartPlugTestBrand.enableMachinePlug() called "
        def disableMachinePlug(self):
                print " SmartPlugTestBrand.disableMachinePlug() called "
        def isMachinePlugEnabled(self):
                print " SmartPlugTestBrand.isMachinePlugPlugEnabled() called "
        def isSwitchedOn(self):
                print " SmartPlugTestBrand.isSwitchedOn() called "

	def manageState(self):
		print "SmartPlugTestBrand.manageState() called"

