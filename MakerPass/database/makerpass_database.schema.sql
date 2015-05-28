PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE machine_rec(machine_id varchar(32), machine_description varchar(127), parent_machine_id varchar(32), plug_id varchar(32));
CREATE TABLE smartplug_rec(plug_id varchar(32), plug_description varchar(127), ip_address varchar(32),  plug_type varchar(127));
CREATE TABLE user_rec(user_id varchar(32), username varchar(32), firstname varchar(32), lastname varchar(32), last_scan DATETIME, total_time_allocated integer, total_time_logged integer);

CREATE TABLE user_machine_scan_rec(username varchar(32), machine_id varchar(32), scan_timestamp DATETIME); 
CREATE TABLE user_machine_allocation_rec(username varchar(32), machine_id varchar(32), last_scan DATETIME, time_allocated integer, time_logged integer); 
CREATE TABLE machine_scanner_table(machine_id varchar(32), scanner_id varchar(32));



COMMIT;
