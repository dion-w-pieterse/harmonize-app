-- :name remove_all_mentions_of_alias_for_blog :affected
DELETE FROM user_blogs_mention WHERE blog_entry_id = :blog_entry_id;