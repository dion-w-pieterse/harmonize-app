-- :name set_forum_response_unlike :affected
DELETE FROM convo_response_like WHERE user_id = :user_id AND convo_response_id = :convo_response_id;