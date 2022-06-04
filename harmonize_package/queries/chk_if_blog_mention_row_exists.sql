-- :name chk_if_blog_mention_row_exists :scalar
select id from user_blogs_mention where blog_entry_id = :blog_entry_id AND user_id = :user_id;