-- :name join_test :many
SELECT public.user.first_name, public.user.last_name, forum_subject.subject_name, thread.title, thread.description
FROM forum_subject
         INNER JOIN public.user ON forum_subject.user_id = public.user.id
         INNER JOIN thread ON thread.subject_id = forum_subject.id