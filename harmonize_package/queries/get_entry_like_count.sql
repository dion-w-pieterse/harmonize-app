-- :name get_entry_like_count :scalar
select COUNT(*)
from blog_entry_like
where blog_entry_id=:blog_entry_id
group by blog_entry_id;