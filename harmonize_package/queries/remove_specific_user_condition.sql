-- :name remove_specific_user_condition :affected
DELETE FROM chosen_condition WHERE condition_name = :condition_name AND user_id = :user_id