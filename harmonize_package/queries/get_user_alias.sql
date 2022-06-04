-- :name get_user_alias :one
SELECT user_alias FROM "public".user WHERE "public".user.user_alias = :user_alias;