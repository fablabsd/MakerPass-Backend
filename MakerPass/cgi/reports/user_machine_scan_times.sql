
/* machine usage per date */
.mode csv
.headers on
select  date(scan_timestamp),machine_id, username, time(scan_timestamp) from user_machine_scan_rec group by 1,2,3,4 order by 1;



