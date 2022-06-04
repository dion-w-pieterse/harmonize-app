-- :name match_out_of_network_specialists :many
select u2.id, u2.user_alias, u2.user_type
from out_of_net_services_for as o
         inner join public.user as u1 on o.insurance_name = u1.chosen_insurance
         inner join public.user as u2 on o.user_id = u2.id
where u1.id = :user_id;