-- :name chk_convo_has_condition_in_db :one
SELECT condition_name
FROM convo_chosen_condition AS ccc
WHERE ccc.condition_name = :condition_name
  AND ccc.conversation_id = :conversation_id;