update user_machine_allocation_rec set inactive_date = date('now');
update user_rec set inactive_date = date('now');

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'chrisanderson', 'FABLAB_CNC1', 9999, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'chrisanderson' and machine_id = 'FABLAB_CNC1'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 439003, 'chrisanderson', 'Chris', 'Anderson', 99999999, date('now') 
where not exists(select username from user_rec where username=
'chrisanderson' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'chrisanderson' and machine_id = 'FABLAB_CNC1'; 

update user_rec set inactive_date = null where username= 
'chrisanderson' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'chrisanderson', 'FABLAB_CNC2', 1000, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'chrisanderson' and machine_id = 'FABLAB_CNC2'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 439003, 'chrisanderson', 'Chris', 'Anderson', 99999999, date('now') 
where not exists(select username from user_rec where username=
'chrisanderson' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'chrisanderson' and machine_id = 'FABLAB_CNC2'; 

update user_rec set inactive_date = null where username= 
'chrisanderson' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'chrisanderson', 'FABLAB_LASER1', 1000, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'chrisanderson' and machine_id = 'FABLAB_LASER1'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 439003, 'chrisanderson', 'Chris', 'Anderson', 99999999, date('now') 
where not exists(select username from user_rec where username=
'chrisanderson' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'chrisanderson' and machine_id = 'FABLAB_LASER1'; 

update user_rec set inactive_date = null where username= 
'chrisanderson' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'chrisanderson', 'TEST_GPIO_MACHINE', 2000, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'chrisanderson' and machine_id = 'TEST_GPIO_MACHINE'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 439003, 'chrisanderson', 'Chris', 'Anderson', 99999999, date('now') 
where not exists(select username from user_rec where username=
'chrisanderson' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'chrisanderson' and machine_id = 'TEST_GPIO_MACHINE'; 

update user_rec set inactive_date = null where username= 
'chrisanderson' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'chrisanderson', 'TEST_GPIO_MACHINE2', 2000, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'chrisanderson' and machine_id = 'TEST_GPIO_MACHINE2'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 439003, 'chrisanderson', 'Chris', 'Anderson', 99999999, date('now') 
where not exists(select username from user_rec where username=
'chrisanderson' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'chrisanderson' and machine_id = 'TEST_GPIO_MACHINE2'; 

update user_rec set inactive_date = null where username= 
'chrisanderson' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'testuser', 'FABLAB_CNC1', 100, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'testuser' and machine_id = 'FABLAB_CNC1'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 274457, 'testuser', 'TestFirst', 'TestLast', 99999999, date('now') 
where not exists(select username from user_rec where username=
'testuser' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'testuser' and machine_id = 'FABLAB_CNC1'; 

update user_rec set inactive_date = null where username= 
'testuser' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'testuser', 'TEST_MACHINE', 1000, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'testuser' and machine_id = 'TEST_MACHINE'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 274457, 'testuser', 'TestFirst', 'TestLast', 99999999, date('now') 
where not exists(select username from user_rec where username=
'testuser' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'testuser' and machine_id = 'TEST_MACHINE'; 

update user_rec set inactive_date = null where username= 
'testuser' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'someuser', 'TEST_MACHINE', 1000, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'someuser' and machine_id = 'TEST_MACHINE'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 12345, 'someuser', 'Some', 'User', 99999999, date('now') 
where not exists(select username from user_rec where username=
'someuser' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'someuser' and machine_id = 'TEST_MACHINE'; 

update user_rec set inactive_date = null where username= 
'someuser' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'someuser', 'TEST_GPIO_MACHINE2', 1000, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'someuser' and machine_id = 'TEST_GPIO_MACHINE2'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 12345, 'someuser', 'Some', 'User', 99999999, date('now') 
where not exists(select username from user_rec where username=
'someuser' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'someuser' and machine_id = 'TEST_GPIO_MACHINE2'; 

update user_rec set inactive_date = null where username= 
'someuser' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'someuser2', 'TEST_GPIO_MACHINE2', 1000, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'someuser2' and machine_id = 'TEST_GPIO_MACHINE2'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 123456, 'someuser2', 'Some', 'User', 99999999, date('now') 
where not exists(select username from user_rec where username=
'someuser2' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'someuser2' and machine_id = 'TEST_GPIO_MACHINE2'; 

update user_rec set inactive_date = null where username= 
'someuser2' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'elliotbuller', 'FABLAB_LASER1', 99999, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'elliotbuller' and machine_id = 'FABLAB_LASER1'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 4920, 'elliotbuller', 'Elliot', 'Buller', 99999999, date('now') 
where not exists(select username from user_rec where username=
'elliotbuller' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'elliotbuller' and machine_id = 'FABLAB_LASER1'; 

update user_rec set inactive_date = null where username= 
'elliotbuller' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'elliotbuller', 'FABLAB_CNC1', 99999, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'elliotbuller' and machine_id = 'FABLAB_CNC1'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 4920, 'elliotbuller', 'Elliot', 'Buller', 99999999, date('now') 
where not exists(select username from user_rec where username=
'elliotbuller' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'elliotbuller' and machine_id = 'FABLAB_CNC1'; 

update user_rec set inactive_date = null where username= 
'elliotbuller' ; 

insert into user_machine_allocation_rec (username, machine_id, time_allocated, active_date) 
select 'elliotbuller', 'TEST_MACHINE', 99998, date('now') 
where not exists(select username, machine_id from user_machine_allocation_rec where username=
'elliotbuller' and machine_id = 'TEST_MACHINE'); 

insert into user_rec (user_id, username, firstname, lastname, total_time_allocated, active_date) 
select 4920, 'elliotbuller', 'Elliot', 'Buller', 99999999, date('now') 
where not exists(select username from user_rec where username=
'elliotbuller' ); 

update user_machine_allocation_rec set inactive_date = null where username= 
'elliotbuller' and machine_id = 'TEST_MACHINE'; 

update user_rec set inactive_date = null where username= 
'elliotbuller' ; 
