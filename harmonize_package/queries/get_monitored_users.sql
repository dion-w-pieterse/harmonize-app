-- :name get_monitored_users :many
SELECT public.user.id, public.user.user_alias, public.user.user_type
FROM monitor AS m
INNER JOIN public.user ON m.monitoree_id = public.user.id
WHERE m.monitor_id = (SELECT id FROM public.user WHERE public.user.id = :monitor_id)
GROUP BY public.user.id, public.user.user_alias, public.user.user_type;