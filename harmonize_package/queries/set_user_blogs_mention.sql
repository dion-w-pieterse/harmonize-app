-- :name set_user_blogs_mention :insert
INSERT INTO user_blogs_mention (blog_entry_id, user_id, created_date) VALUES (:blog_entry_id, :user_id, CURRENT_TIMESTAMP at time zone 'utc');