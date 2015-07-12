#!/usr/bin/python


import RPi.GPIO as GPIO

from MachinePlug_2State import MachinePlug_2State
from MachineStates import MachineStates
from MakerPassLogger import MachinePlug_GPIO_logger as logger

class MachinePlug_GPIO(MachinePlug_2State):

        
	def __init__(self, machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold):
		super(MachinePlug_GPIO, self).__init__(machine_id, machine_desc, plug_id, plug_desc, plug_type, plug_name, machine_power_threshold)

		## map the "plug_name" to a specific BCM numbered gpio pin
		self.GPIO_MAP = {'GPIOPLUG5': 5, 'GPIOPLUG6': 6,'GPIOPLUG12': 12,'GPIOPLUG13': 13,'GPIOPLUG16': 16,'GPIOPLUG17': 17,'GPIOPLUG18': 18,'GPIOPLUG19': 19,'GPIOPLUG20': 20,'GPIOPLUG21': 21,'GPIOPLUG22': 22,'GPIOPLUG23': 23,'GPIOPLUG24': 24,'GPIOPLUG25': 25,'GPIOPLUG26': 26, 'GPIOPLUG27': 27}

		self.GPIO_NUM = self.GPIO_MAP[plug_name]
		logger.debug(" MachinePlug_GPIO using gpio number " + str(self.GPIO_NUM))

			
        ##  ----- METHODS -------------------------------------

        def doEnableMachinePlug(self):
                
		logger.debug( " MachinePlug_GPIO.doEnableMachinePlug() called ")

		# use P1 header pin numbering convention
		GPIO.setmode(GPIO.BCM)
	
		# Set up the GPIO channels
		GPIO.setup(self.GPIO_NUM, GPIO.OUT)

		## set GPIO high
		GPIO.output(self.GPIO_NUM, GPIO.HIGH)

       
	def doDisableMachinePlug(self):
                
		logger.debug( " MachinePlug_GPIO.doDisableMachinePlug() called ")

		# use P1 header pin numbering convention
		GPIO.setmode(GPIO.BCM)
	
		# Set up the GPIO channels
		GPIO.setup(self.GPIO_NUM, GPIO.OUT)

		# set GPIO low		
		GPIO.output(self.GPIO_NUM, GPIO.LOW)





 
