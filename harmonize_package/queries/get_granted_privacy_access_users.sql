-- :name get_granted_privacy_access_users :many
SELECT public.user.id, public.user.user_alias, public.user.user_type
FROM granted_privacy_access AS gpa
INNER JOIN public.user ON gpa.grantee_id = public.user.id
WHERE gpa.grantor_id = (SELECT id FROM public.user WHERE public.user.id = :grantor_id)
GROUP BY public.user.id, public.user.user_alias, public.user.user_type;