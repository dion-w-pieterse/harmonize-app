-- :name get_user_id_by_alias :one
SELECT id FROM "public".user WHERE "public".user.user_alias = :user_alias;