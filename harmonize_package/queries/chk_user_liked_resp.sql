-- :name chk_user_liked_resp :one
SELECT *
FROM convo_response_like AS crl
WHERE crl.user_id = :user_id
  AND crl.convo_response_id = :convo_response_id;