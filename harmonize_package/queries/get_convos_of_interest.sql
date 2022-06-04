-- :name get_convos_of_interest :many
SELECT DISTINCT convo.*, public.user.user_alias, fr.room_name
FROM conversation AS convo
INNER JOIN convo_chosen_condition AS convo_cc ON convo.id = convo_cc.conversation_id
INNER JOIN chosen_condition AS cc ON convo_cc.condition_name = cc.condition_name
INNER JOIN public.user on convo.user_id = public.user.id
INNER JOIN forum_room AS fr on convo.forum_room_id = fr.id
WHERE cc.user_id = :user_id
ORDER BY created_date DESC, public.user.user_alias;