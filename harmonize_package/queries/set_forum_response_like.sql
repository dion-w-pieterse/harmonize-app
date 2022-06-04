-- :name set_forum_response_like :insert
INSERT INTO convo_response_like (user_id, convo_response_id) VALUES (:user_id, :convo_response_id);