-- :name set_blog_entry_like :insert
INSERT INTO blog_entry_like (user_id, blog_entry_id) VALUES (:user_id, :blog_entry_id);