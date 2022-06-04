-- :name get_grantor_private_access_user_journals :many
SELECT be.id, be.title, be.entry_img, be.body, be.private_entry, be.created_date, be.user_id,
       public.user.user_alias, public.user.user_type
FROM blog_entry AS be
         INNER JOIN granted_privacy_access AS gpa ON be.user_id = gpa.grantor_id
         INNER JOIN public.user ON gpa.grantor_id = public.user.id
WHERE gpa.grantee_id = (SELECT id FROM public.user WHERE public.user.id = :grantee_id)
ORDER BY be.created_date DESC, public.user.user_alias;