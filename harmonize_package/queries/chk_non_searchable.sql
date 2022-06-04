-- :name chk_non_searchable :one
SELECT non_searchable
FROM public.user
WHERE id = :user_id and non_searchable = True;