
TARGET = makerpass


all:
	@echo  
	@echo "Use make install or uninstall" 
	@echo  

install: 
	[ "`id -u`" = "0" ] || { echo "Must be run as root"; exit 1; }
	cp -f init-script /etc/init.d/$(TARGET)
	chmod 755 /etc/init.d/$(TARGET)
	update-rc.d $(TARGET) defaults 92 08
	#/etc/init.d/$(TARGET) start

uninstall:
	[ "`id -u`" = "0" ] || { echo "Must be run as root"; exit 1; }
	[ -e /etc/init.d/$(TARGET) ] && /etc/init.d/$(TARGET) stop || :
	update-rc.d $(TARGET) remove
	rm -f /etc/init.d/$(TARGET)

