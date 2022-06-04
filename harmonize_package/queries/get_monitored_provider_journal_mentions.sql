-- :name get_monitored_provider_journal_mentions :many
SELECT public.user.id, public.user.user_alias, public.user.user_type, ubm.blog_entry_id, be.title, ubm.created_date
FROM user_blogs_mention AS ubm
         INNER JOIN blog_entry AS be ON ubm.blog_entry_id = be.id
         INNER JOIN public.user ON ubm.user_id = public.user.id
WHERE ubm.user_id IN (SELECT monitoree_id FROM monitor WHERE monitor_id = :current_user_id)
  AND be.created_date BETWEEN
    (be.created_date - INTERVAL '7 day') AND (CURRENT_TIMESTAMP at time zone 'utc')
  AND public.user.user_type = 'provider'
ORDER BY ubm.created_date DESC