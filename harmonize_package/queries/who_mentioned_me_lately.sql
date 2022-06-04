-- :name who_mentioned_me_lately :many
SELECT id, user_alias, user_type, SUM(blog_mention_count) AS blog_mention_count, SUM(convo_response_count) AS convo_response_count
FROM (
         SELECT public.user.id AS id, public.user.user_alias AS user_alias, public.user.user_type AS user_type, COUNT(ubm.blog_entry_id) AS blog_mention_count, 0 AS convo_response_count
         FROM user_blogs_mention AS ubm
                  INNER JOIN blog_entry AS be ON ubm.blog_entry_id = be.id
                  INNER JOIN public.user ON be.user_id = public.user.id
         WHERE ubm.user_id = :current_user_id
           AND be.created_date BETWEEN
             (be.created_date - INTERVAL '7 day') AND (CURRENT_TIMESTAMP at time zone 'utc')
         GROUP BY public.user.id, public.user.user_alias, public.user.user_type
         UNION ALL
         SELECT public.user.id, public.user.user_alias, public.user.user_type, 0 AS blog_entry_id, COUNT(ufm.convo_response_id)
         FROM user_forum_mention AS ufm
                  INNER JOIN convo_response AS cr ON ufm.convo_response_id = cr.id
                  INNER JOIN public.user ON cr.user_id = public.user.id
         WHERE ufm.user_id = :current_user_id
           AND cr.created_date BETWEEN
             (cr.created_date - INTERVAL '7 day') AND (CURRENT_TIMESTAMP at time zone 'utc')
         GROUP BY public.user.id, public.user.user_alias, public.user.user_type
     ) b
GROUP BY id, user_alias, user_type