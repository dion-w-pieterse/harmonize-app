-- :name chk_user_insurance_choice_is_in_db :one
SELECT insurance_name
FROM out_of_net_services_for AS oonsf
WHERE oonsf.insurance_name = :insurance_name
  AND oonsf.user_id = :user_id;