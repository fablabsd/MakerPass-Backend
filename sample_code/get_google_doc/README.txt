


How to get downloadable URL for document on google drive:
Get the publicly "shareable" link:
In that link there will be a document ID...it's the gobble-dee-gook.

For regular documents you can use this:
Extract the ID and insert it into this URL
https://www.googledrive.com/host/<DOC_ID>
Navigate to that URL in your browser and you will be redirected to the (very long) raw URL for your doc.   
You can now auto-download this with wget like so:
wget --no-check-certificate <super_long_url>  -O output_file_name

For "google" docs like spreadsheets etc, you must use a different download URL.  
For example:

wget --no-check-certificate https://docs.google.com/spreadsheets/d/1LyYnzCeJLjo9D6G46-hchiET48JVcDIRTxq5Ee-dhaE/export?format=csv -O ./temp.csv


There are differnent URL types for different types of docs.  For more info go here:
http://www.labnol.org/internet/direct-links-for-google-drive/28356/


