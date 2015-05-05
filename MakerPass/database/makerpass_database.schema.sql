PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE machine_rec(machine_id varchar(32), description varchar(127), parent_machine varchar(32), plug_id varchar(32));
CREATE TABLE smartplug_rec(plug_id varchar(32), description varchar(127), ip_address varchar(32), statemap_type varchar(32));
CREATE TABLE statemap_types_table(statemap_type varchar(32), description varchar(127));
CREATE TABLE user_rec(user_id varchar(32), username varchar(32), firstname varchar(32), lastname varchar(32), last_scan text, total_time_left integer, total_time_logged integer);

CREATE TABLE user_machine_scan_rec(user_id varchar(32), machine_id varchar(32), scan_timestamp text); 
CREATE TABLE user_machine_allocation_rec(user_id varchar(32), machine_id varchar(32), last_scan text time_left integer, time_logged integer); 



COMMIT;
