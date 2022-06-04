-- :name chk_if_forum_mention_row_exists :scalar
select id from user_forum_mention where convo_response_id = :convo_response_id AND user_id = :user_id;