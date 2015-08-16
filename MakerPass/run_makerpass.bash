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

## create the user_feedback.txt file if it doesn't already exist, and ensure
## that it is readable by the pi user (for cgi access)
echo "Creating cgi/user_feedback.txt"
touch $BASE_PATH/cgi/user_feedback.txt
chown pi:pi $BASE_PATH/cgi/user_feedback.txt 
chmod 777 $BASE_PATH/cgi/user_feedback.txt

## create the pipe_scan fifo/pipe which will accept scan-ins from 
## any other process/location (but mainly from HUD.cgi)
## we re-create this here so as to eliminate the possibility of 
## zombie scans living in the pipe getting registered on start-up
echo "Creating pipe_scan fifo"
rm -f $BASE_PATH/pipe_scan
mkfifo $BASE_PATH/pipe_scan
chmod 666 $BASE_PATH/pipe_scan

## Same as above here for wifi_scan (for WifiPipe.py) and wifi_response
## for scans coming in from cgi/registerscan.cgi
echo "Creating wifi_scan fifo and wifi_response fifo"
rm -f $BASE_PATH/wifi_scan $BASE_PATH/wifi_response
mkfifo $BASE_PATH/wifi_scan $BASE_PATH/wifi_response
chmod 666 $BASE_PATH/wifi_scan $BASE_PATH/wifi_response

 
## run the main thread which will spawn the reader threads for scanner input
## the cluster controller id  for this instance is in cluster_controller.config
echo "Spawning main makerpass process"
sudo python $BASE_PATH/main.py 



