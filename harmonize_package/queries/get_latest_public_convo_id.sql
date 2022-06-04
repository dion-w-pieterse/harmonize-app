-- :name get_latest_public_convo_id :scalar
select max(id) from conversation;