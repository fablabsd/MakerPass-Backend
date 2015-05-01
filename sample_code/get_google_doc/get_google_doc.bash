

## The document ID is everything after the /d and before /export -- this can be obtained from the 
## shareable link.  There are other types of URLs for different doc types - this is just for spreadsheets

echo "Doing wget of google doc into temp.csv file"
wget --no-check-certificate https://docs.google.com/spreadsheets/d/1LyYnzCeJLjo9D6G46-hchiET48JVcDIRTxq5Ee-dhaE/export?format=csv -O ./temp.csv

