-- :name get_latest_blog_entry_id :scalar
select max(id) from blog_entry;