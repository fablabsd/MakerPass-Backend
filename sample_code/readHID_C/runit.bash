#!/bin/bash

## set gpio out
sudo gpio mode 1 out

## write ready to lcd
sudo adafruit-rpi-lcd -c white "Ready..."

## wait for swipe -- note hidraw device listed below
## is dynamic, so you may need to try hidraw0,1,2 etc...
## grep for keyboard in dmesg and look for a keyboard belonging to STMicroelectronics
## i.e. keyboard emulated swipe
sudo ./a.out /dev/hidraw1 | sudo perl swipe.pl

## turn off lcd and machine/led
sudo adafruit-rpi-lcd --off
sudo gpio write 1 0

