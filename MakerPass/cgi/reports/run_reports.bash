#!/bin/bash

DB_FILE=/home/pi/makerpass/MakerPass/database/makerpass_database.db

cat machine_usage_per_person.sql | sqlite3 $DB_FILE > machine_usage_per_person.csv
cat machine_usage_per_date.sql | sqlite3 $DB_FILE > machine_usage_per_date.csv
cat user_machine_scan_times.sql | sqlite3 $DB_FILE > user_machine_scan_times.csv 



