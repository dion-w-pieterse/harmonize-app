-- :name get_monitored_journal_entries :many
SELECT be.id, be.title, be.entry_img, be.body, be.private_entry, be.created_date, be.user_id, public.user.user_alias
FROM blog_entry AS be
         JOIN monitor AS m ON be.user_id = m.monitoree_id
         LEFT OUTER JOIN public.user ON m.monitoree_id = public.user.id
WHERE m.monitor_id = (SELECT id FROM public.user WHERE public.user.id = :monitor_id)
AND be.user_id IN (SELECT id FROM public.user WHERE user_type = 'patient')
ORDER BY be.created_date DESC, public.user.user_alias;