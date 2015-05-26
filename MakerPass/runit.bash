#!/bin/bash

## First discover which port the mag stripe scanner is connected to..
/bin/dmesg | \grep STMicroelectronics | \grep Keyboard | cut -d"," -f2 | cut -d":" -f1 > magstripe_scan_usb_port.config


## Set ID for this master/cluster controller - this should match whichever 
## machine ID in the database you intend to control the indicated machines

sudo env MY_MASTER_CONTROLLER_ID=MASTER_CONTROLLER python ./main.py


