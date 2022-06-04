-- :name get_monitoree_entries :many
SELECT be.id, be.title, be.entry_img, be.body, be.private_entry, be.created_date, public.user.user_alias
FROM blog_entry AS be
         JOIN monitor AS m ON be.user_id = m.monitor_id
         LEFT OUTER JOIN public.user ON m.monitor_id = public.user.id
WHERE m.monitoree_id = (SELECT id FROM public.user WHERE public.user.id = :monitoree_id);