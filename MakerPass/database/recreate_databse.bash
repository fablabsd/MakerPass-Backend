#!/bin/bash

################################################################
## WARNING:  executing this cript will completely re-initialize 
## the database from scratch and all previous data will be lost
## A backup is made as a .bak file and can be restored
#################################################################


## remove existing database and data file for a clean create
echo "Backing up existing database file:  makerpass_database.db"
\mv -f makerpass_database.db makerpass_database.db.bak

## create the tables in the database (database created automatically)
echo "Creating database tables"
cat makerpass_database.schema.sql | sqlite3 makerpass_database.db


## reimport those records we are controlling from spreadsheets/CSVs
./reimport_db_config_recs.bash
