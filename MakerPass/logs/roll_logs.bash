#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d%H%M")
BASEPATH=/home/pi/makerpass/MakerPass/logs

## remove logs older than 30 days -- this script is called 
## from /etc/cron.daily (i.e. used by anacron to run even 
## if machine was off during normal time to be run)
#find /home/pi/makerpass/MakerPass/logs/archive/ -name "makerpass.log.*" -mtime +30 -exec rm -f {} \;
find $BASEPATH/archive/ -name "makerpass.log.*" -mmin +30 -exec rm -f {} \;


## back up the current log into a timestamped version
cp $BASEPATH/current_makerpass.log $BASEPATH/archive/makerpass.log.$TIMESTAMP

## clear out the current log (note this may not be 
## an open-platform operation, but seems to work here
## even while makerpass is running)
echo "" > $BASEPATH/current_makerpass.log


