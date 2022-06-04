-- :name get_user :one
SELECT * FROM "public".user WHERE "public".user.id = :user_id;