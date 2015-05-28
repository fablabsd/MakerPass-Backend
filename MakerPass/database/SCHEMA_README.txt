
//defines the machine being controlled 
<machines>
	<machine_id>
	<description>
	<parent_id>...this is important for configuring if we are using a centralized or de-centralized design...if centralized, then only one master for a group of machines...if decentralized then each machine is it's own master, and controls only one plug
	<plug_id> ...i.e. foreign key code to plug that maps to ip_address of it's smartplug

</machines>

// defines the different smartplugs usable by a machine
<smartplugs>
	<plug_id>
	<friendly_name>...i.e. "WeMo Insight"
	<ip_address>
	<statemap_type>...i.e. just on/off, or on_off_w_power_monitor etc
</smartplugs>

// defines the kind of statemap that will get used to control a plug (this depends on the plug's capabilities)
<statemap_types>
	<statemap_type>...i.e. ON_OFF or ON_OFF_W_POWER_MONITOR
	<description>...i.e. this statemap only supports binary on/off controls...or this statemap supports multiple features requiring power monitoring...

</statemap_types>

// user overview
<users>
	<user_id> // for barcode
	<username> // for potential future use with active directory or other authentication tool
	<firstname>
	<lastname>
	<last_scan>  // text field w datetime
	<total_time_left> // for counting down allocation (assumes one allocation for all machines)
	<total_time_logged> // quick view to see user's total timed used for all machines

</users>

// shows scans made to individual machines by an individual user	
<user_machine_scans>
	<user_id>
	<machine_id>
	<scan_timestamp>  // text datetime field of an individual scan

</user_machine_scans>	

// show allocation for individual machines for an individual user
<user_machine_allocations>
	<user_id>
	<machine_id>
	<last_scan>
	<time_left>
	<time_logged>

</user_machine_allocations>

// map a specific machine to a specific scanning device
<machine_scanner_table>
	<machine_id>
	<scanner_id>
</machine_scanner_table>
