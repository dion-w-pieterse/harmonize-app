-- :name select_user_test :one
select blog_entry.title, blog_entry.body, blog_entry.created_date from blog_entry where id = :id_arg