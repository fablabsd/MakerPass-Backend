
/* machine usage per person */
.mode csv
.headers on
select * from user_machine_allocation_rec where inactive_date is null;



