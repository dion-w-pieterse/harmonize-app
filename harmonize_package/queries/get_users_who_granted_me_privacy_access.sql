-- :name get_users_who_granted_me_privacy_access :many
SELECT public.user.id, public.user.user_alias, public.user.user_type
FROM granted_privacy_access AS gpa
         INNER JOIN public.user ON gpa.grantor_id = public.user.id
WHERE gpa.grantee_id = (SELECT id FROM public.user WHERE public.user.id = :grantee_id)
GROUP BY public.user.id, public.user.user_alias, public.user.user_type;