-- :name get_monitored_provider_forum_mentions :many
SELECT public.user.id, public.user.user_alias, public.user.user_type, ufm.convo_response_id, con.id AS convo_id, con.forum_room_id
FROM user_forum_mention AS ufm
         INNER JOIN convo_response AS cr ON ufm.convo_response_id = cr.id
         INNER JOIN public.user ON ufm.user_id = public.user.id
         INNER JOIN conversation AS con ON cr.conversation_id = con.id
         INNER JOIN forum_room AS fr ON con.forum_room_id = fr.id
WHERE ufm.user_id IN (SELECT monitoree_id FROM monitor WHERE monitor_id = :current_user_id)
  AND cr.created_date BETWEEN
    (cr.created_date - INTERVAL '7 day') AND (CURRENT_TIMESTAMP at time zone 'utc')
  AND public.user.user_type = 'provider'