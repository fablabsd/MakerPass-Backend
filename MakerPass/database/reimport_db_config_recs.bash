#!/bin/bash

## This file will re-create/import data from google doc spreadsheets
## into the makerpass database

MACHINE_REC_DOC_ID=1RvGX6tUAwSgrQtyrX9FeFCpgfk7ni_uVwMdaHbe-jMg
USER_REC_DOC_ID=1JjraMUDdcFVLjQb9q7wPXU-NcLepafx_40wkSUFO8XI
USER_MACHINE_ALLOCATION_REC_DOC_ID=1FhCMCNqi-xXgo7yVSg9yA4Woy6nVRj4HoormwlXbOjk
SMARTPLUG_REC_DOC_ID=1w9wufdd8C0z37o5xJRUldUehYc7iCydzgRC67ApYM8E

## download data from google docs
echo "Downloading database CSV files from google docs"
echo "Downloading machine_rec.csv"
wget --quiet --no-check-certificate https://docs.google.com/spreadsheets/d/$MACHINE_REC_DOC_ID/export?format=csv -O ./machine_rec.csv

echo "Downloading user_rec.csv"
wget --quiet --no-check-certificate https://docs.google.com/spreadsheets/d/$USER_REC_DOC_ID/export?format=csv -O ./user_rec.csv

echo "Downloading user_machine_allocation_rec.csv"
wget --quiet --no-check-certificate https://docs.google.com/spreadsheets/d/$USER_MACHINE_ALLOCATION_REC_DOC_ID/export?format=csv -O ./user_machine_allocation_rec.csv

echo "Downloading smartplug_rec.csv"
wget --quiet --no-check-certificate https://docs.google.com/spreadsheets/d/$SMARTPLUG_REC_DOC_ID/export?format=csv -O ./smartplug_rec.csv


## strip off header line of csv files
sed -i '1d' machine_rec.csv
sed -i '1d' user_rec.csv
sed -i '1d' user_machine_allocation_rec.csv
sed -i '1d' smartplug_rec.csv


## Delete and re-import data into the database
echo "Deleting existing data and Re-importing data from CSVs"
cat data_import_commands.import | sqlite3 makerpass_database.db

## display results
echo ""
echo "Sample output:"
echo ""
echo "machine_rec:"
echo "select * from machine_rec limit 5;" | sqlite3 makerpass_database.db
echo ""
echo ""
echo "user_rec:"
echo "select * from user_rec limit 5;" | sqlite3 makerpass_database.db
echo ""
echo ""
echo "user_machine_allocation_rec:"
echo "select * from user_machine_allocation_rec limit 5;" | sqlite3 makerpass_database.db
echo ""
echo ""
echo "smartplug_rec:"
echo "select * from smartplug_rec limit 5;" | sqlite3 makerpass_database.db
echo ""
echo ""


