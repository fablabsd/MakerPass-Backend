#!/usr/bin/perl -w


#==============================================================================#
# Load Needed Libraries
#------------------------------------------------------------------------------#

use strict;
use POSIX qw(strftime);
#use warnings;
#use diagnostics;

#use IO::Socket::SSL;
#use Mail::IMAPClient;
my $id = 0;
my %keymap = ('39' => 0, '30' => 1, '31' => 2,'32' => 3,'33' => 4,'34' => 5,'35' => 6,'36' => 7,'37' => 8,'38' => 9); 
my @valid_ids = (100810, 439003, 292667); ##, 704429);
my @machine_access = ('Y', 'Y', 'Y', 'Y');
my @credit_left = (50, 100, 125, 100);
my $now_string = "";
my $lcd_cmd = "";
my $machine_on = 0;
my $active_ID = 0;

## read swipe string
while (my $swipe_string = <STDIN>) { 

#print $swipe_string;
my @chars = split(" ", $swipe_string);
print "chars:  $chars[10]$chars[11]$chars[12]$chars[13]$chars[14]$chars[15]\n";
$id = $keymap{$chars[10]} . $keymap{$chars[11]} . $keymap{$chars[12]} . $keymap{$chars[13]} . $keymap{$chars[14]} . $keymap{$chars[15]};



## search for existence of ID
my $i;
my $id_exists = 0;
for ($i = 0; $i < @valid_ids; $i++) {
	if ($valid_ids[$i] eq $id) { $id_exists = 1; last; }
}

## fail if ID is invalid
if (!$id_exists) { 
	print "ID:  $id does not exist\n"; 
	$lcd_cmd = "adafruit-rpi-lcd -c red \"ID: $id      ID NOT FOUND\"";
	system $lcd_cmd;
	## turn off machine
	system "gpio write 1 0";
	$machine_on = 0;
	next; 
}

## fail if ID has no access to this machine
if (!($machine_access[$i] eq "Y")) { 
	print "ID:  $id does not have access to this machine\n"; 
	$lcd_cmd = "adafruit-rpi-lcd -c red \"ID: $id      NO ACCESS FOR ID\"";
	system $lcd_cmd;
	## turn off machine
	system "gpio write 1 0";
	$machine_on = 0;
	next; 
} 

## success...show output of ID and timestamp
$now_string = strftime "%H:%M:%S", localtime;

## if machine is off show turning on status
if ($machine_on == 0) {

	print "ID: $id\n";
	print "start time:  $now_string\n";

	## write to LCD
	$lcd_cmd = "adafruit-rpi-lcd -c cyan \"ID: $id      START: $now_string\"";
	system $lcd_cmd;

	## turn on machine
	$machine_on = 1;
	system "gpio write 1 1";

} else { ## machine is on - 

	## same user...
	if ($active_ID == $id) { 
	        print "ID: $id\n";
		print "stop time:  $now_string\n";

        	## write to LCD
        	$lcd_cmd = "adafruit-rpi-lcd -c cyan \"ID: $id      STOP: $now_string\"";
        	system $lcd_cmd;

        	## turn off machine
		$machine_on = 0;
        	system "gpio write 1 0";
	
	## different user
	} else {
	        print "ID: $id\n";
        	print "start time:  $now_string\n";

        	## write to LCD
        	$lcd_cmd = "adafruit-rpi-lcd -c cyan \"ID: $id      START: $now_string\"";
        	system $lcd_cmd;

	}

} ## end if 

$active_ID = $id;

} ## end while

exit;

