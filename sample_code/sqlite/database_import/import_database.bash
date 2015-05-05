
## remove existing database and data file for a clean create
\rm -f machine_config.db machine_config.csv

## download data from google docs
wget --no-check-certificate https://docs.google.com/spreadsheets/d/1LyYnzCeJLjo9D6G46-hchiET48JVcDIRTxq5Ee-dhaE/export?format=csv -O ./machine_config.csv

## create the tables in the database (database created automatically)
cat database_schema.schema | sqlite3 machine_config.db

## import data into the database
cat database_commands.import | sqlite3 machine_config.db

## display results
echo "select * from machine_config;" | sqlite3 machine_config.db


