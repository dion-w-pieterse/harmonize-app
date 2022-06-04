-- :name set_user_forum_mention :insert
INSERT INTO user_forum_mention (convo_response_id, user_id, created_date) VALUES (:convo_response_id, :user_id, CURRENT_TIMESTAMP at time zone 'utc');