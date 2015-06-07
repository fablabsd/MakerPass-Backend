select * 
from machine_rec 
join smartplug_rec on (smartplug_rec.plug_id = machine_rec.plug_id) 
left join user_machine_allocation_rec on (user_machine_allocation_rec.machine_id = machine_rec.machine_id) 
where current_user=username

union

select *
from machine_rec
join smartplug_rec on (smartplug_rec.plug_id = machine_rec.plug_id)
left join user_machine_allocation_rec on (user_machine_allocation_rec.machine_id = machine_rec.machine_id)
where (current_user = '' or current_user = 'none')

;
