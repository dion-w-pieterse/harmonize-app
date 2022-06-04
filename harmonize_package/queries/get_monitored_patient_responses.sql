-- :name get_monitored_patient_responses :many
SELECT cr.id, cr.resp_img, cr.body, cr. private_response, cr.created_date, cr.user_id, public.user.user_alias, cr.conversation_id, con.convo_name, con.forum_room_id, fr.room_name
FROM convo_response AS cr
INNER JOIN conversation AS con ON cr.conversation_id = con.id
INNER JOIN forum_room AS fr ON con.forum_room_id = fr.id
INNER JOIN public.user ON cr.user_id = public.user.id
WHERE cr.user_id IN (SELECT monitoree_id FROM monitor WHERE monitor_id = :monitor_id)
AND public.user.user_type = 'patient'
ORDER BY cr.created_date DESC, public.user.user_alias ASC;