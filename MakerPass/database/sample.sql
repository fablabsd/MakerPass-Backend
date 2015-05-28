

/*select username from user_rec where user_id=123456;*/

/*
select 
*
from 
user_machine_allocation_rec 
where 
username = 'testuser'
and machine_id = 'FABLAB_CNC2' ;
*/

/*
insert into user_machine_scan_rec (username, machine_id, scan_timestamp) values ('testuser', 'FABLAB_LASER1', (DATETIME('now')));
*/ 


select * from user_machine_scan_rec;
select * from user_rec;


/*
update user_machine_allocation_rec set last_scan = (DATETIME('now')) where username = 'testuser' and machine_id = 'FABLAB_CNC1';

*/
