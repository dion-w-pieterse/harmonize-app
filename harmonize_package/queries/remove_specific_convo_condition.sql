-- :name remove_specific_convo_condition :affected
DELETE FROM convo_chosen_condition WHERE condition_name = :condition_name AND conversation_id = :conversation_id