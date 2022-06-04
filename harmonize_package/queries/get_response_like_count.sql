-- :name get_response_like_count :scalar
select COUNT(*)
from convo_response_like
where convo_response_id=:convo_response_id
group by convo_response_id;