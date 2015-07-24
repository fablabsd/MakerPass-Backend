#!/bin/bash

## This file will re-create/import data from a google doc spreadsheet
## into the makerpass database

BASE_DIR=/home/pi/makerpass/MakerPass/database/user_import
USER_IMPORT_DOC_ID=1w8ZCohZG1TiZGBf5kuWfb60wRoelQkLzJvvz8NVa2AQ


## download data from google docs
echo "Downloading user_import.csv from google docs"
wget --quiet --no-check-certificate https://docs.google.com/spreadsheets/d/$USER_IMPORT_DOC_ID/export?format=csv -O $BASE_DIR/user_import.csv

## create import sqls from import data file 
## this will extract the info from user_import.csv
echo "Creating generated sql file"
python $BASE_DIR/user_import.py > $BASE_DIR/user_import.sql 

## before making this import official, make a quick sanity backup of the database
echo "Backing up database"
cp $BASE_DIR/../makerpass_database.db $BASE_DIR/../makerpass_database.db.pre-user-import

## run the generated sqls against makerpass to 
## create a master list / system of record
echo "Executing sqls"
cat $BASE_DIR/user_import.sql | sqlite3 $BASE_DIR/../makerpass_database.db

echo "Done"
