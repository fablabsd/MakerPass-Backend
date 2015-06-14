
import random
import datetime
import time
import ouimeaux
from ouimeaux.environment import Environment

# http://pydoc.net/Python/ouimeaux/0.7.3/ouimeaux.examples.watch/
if __name__ == "__main__":
    print ""
    print "---------------"
    env = Environment(with_cache=False, bind=None)
    # TODO: run from 10am to 10pm
    try:
	print "calling env.start()"
        env.start()
	print "calling env.discover()"
        env.discover(15)
	print "listing switches"
        print env.list_switches()
        #print env.list_motions()
        print "---------------"
        #while True:
            # http://stackoverflow.com/questions/306400/how-do-i-randomly-select-an-item-from-a-list-using-python
            #switchRND = env.get_switch( random.choice( env.list_switches() ) )
	print "calling get_switch()"
        switchRND = env.get_switch( "WEMO CNC ROOM" )
        print switchRND
	power = switchRND.current_power
	print "turning off"
	switchRND.basicevent.SetBinaryState(BinaryState=0)
	print "turning on"
	switchRND.basicevent.SetBinaryState(BinaryState=1)
	#switchRND.explain()
	print switchRND.deviceinfo.GetDeviceInformation()
	print switchRND.basicevent.GetDeviceId()
	print "power = " + str(power)
	print "mac address = " + str(switchRND.basicevent.GetMacAddr())
        #switchRND.toggle()
	print "waiting.."
        env.wait(1)
        
    except (KeyboardInterrupt, SystemExit):
        print "---------------"
        print "Goodbye!"
        print "---------------"
        # Turn off all switches
        for switch in ( env.list_switches() ):
            print "Turning Off: " + switch
            env.get_switch( switch ).off()
