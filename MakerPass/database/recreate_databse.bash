
## remove existing database and data file for a clean create
\mv -f makerpass_database.db makerpass_database.db.bak

## download data from google docs
wget --no-check-certificate https://docs.google.com/spreadsheets/d/1LyYnzCeJLjo9D6G46-hchiET48JVcDIRTxq5Ee-dhaE/export?format=csv -O ./machine_rec.csv

## strip off header line of file
sed -i '1d' machine_rec.csv

## create the tables in the database (database created automatically)
cat makerpass_database.schema.sql | sqlite3 makerpass_database.db

## import data into the database
cat database_commands.import | sqlite3 makerpass_database.db

## display results
echo "select * from machine_rec;" | sqlite3 makerpass_database.db


