-- :name chk_user_has_condition_in_db :one
SELECT condition_name
FROM chosen_condition AS cc
WHERE cc.condition_name = :condition_name
  AND cc.user_id = :user_id;