-- :name recommend_patient_to_patient_associations :many
select distinct public.user.id, public.user.user_alias, public.user.user_type
from public.user
         inner join chosen_condition as cc on public.user.id = cc.user_id
where cc.condition_name in (select condition_name from chosen_condition where user_id = :current_user_id)
  and public.user.id <> :current_user_id
and public.user.user_type = 'patient';