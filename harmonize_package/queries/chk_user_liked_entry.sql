-- :name chk_user_liked_entry :one
SELECT *
FROM blog_entry_like AS bel
WHERE bel.user_id = :user_id
  AND bel.blog_entry_id = :blog_entry_id;