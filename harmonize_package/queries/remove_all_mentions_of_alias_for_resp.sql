-- :name remove_all_mentions_of_alias_for_resp :affected
DELETE FROM user_forum_mention WHERE convo_response_id = :convo_response_id;