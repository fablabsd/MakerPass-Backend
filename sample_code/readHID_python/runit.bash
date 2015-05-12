#!/bin/bash


## note device is dynamic so may not be hidraw1 - grep for 
## keyboard in dmesg and look for which hidraw device belongs to STMmicroelectronics 
sudo python readSTMKeyboardHID.py /dev/hidraw1
