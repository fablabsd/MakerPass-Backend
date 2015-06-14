


all:
	@echo  
	@echo "Use make install or uninstall" 
	@echo  

install: 
	[ "`id -u`" = "0" ] || { echo "Must be run as root"; exit 1; }
	## install makerpass
	cp -f init-script-makerpass /etc/init.d/makerpass
	chmod 755 /etc/init.d/makerpass
	update-rc.d makerpass defaults 92 08
	#/etc/init.d/makerpass start
	## install LED watchdog
	cp -f init-script-LEDwatchdog /etc/init.d/LEDwatchdog
	chmod 755 /etc/init.d/LEDwatchdog
	update-rc.d LEDwatchdog defaults 92 08
	#/etc/init.d/LEDwatchdog start

uninstall:
	[ "`id -u`" = "0" ] || { echo "Must be run as root"; exit 1; }
	## uninstall makerpass
	[ -e /etc/init.d/makerpass ] && /etc/init.d/makerpass stop || :
	update-rc.d makerpass remove
	rm -f /etc/init.d/makerpass
	## uninstall LEDwatchdog
	[ -e /etc/init.d/LEDwatchdog ] && /etc/init.d/LEDwatchdog stop || :
	update-rc.d LEDwatchdog remove
	rm -f /etc/init.d/LEDwatchdog

