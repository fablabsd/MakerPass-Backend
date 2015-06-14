#!/bin/bash


BASE_PATH=/home/pi/makerpass/MakerPass


## First discover which port the mag stripe scanner is connected to..
echo "Discovering scan/swipe device(s)"
/bin/dmesg | \grep STMicroelectronics | \grep Keyboard | cut -d"," -f2 | cut -d":" -f1 > $BASE_PATH/magstripe_scan_usb_port.config

## clear the wemo cache -- wemo is unstable whenever a plug falls off the system, 
## so this resets the list of plugs
echo "Clearing Wemo Cache"
wemo clear

cd $BASE_PATH

## run the main thread which will spawn the reader threads for scanner input
## the cluster controller id  for this instance is in cluster_controller.config
echo "Spawning main makerpass process"
sudo python $BASE_PATH/main.py 



