-- :name set_blog_entry_unlike :affected
DELETE FROM blog_entry_like WHERE user_id = :user_id AND blog_entry_id = :blog_entry_id;