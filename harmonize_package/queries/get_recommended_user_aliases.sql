-- :name get_recommended_user_aliases :many
SELECT public.user.user_alias FROM public.user
WHERE
LEFT(user_alias,3) = LEFT(:user_alias,3)
OR
RIGHT(user_alias,4) = RIGHT(:user_alias,4)
OR
LEFT(user_alias,6) = LEFT(:user_alias,6)
OR
RIGHT(user_alias,6) = RIGHT(:user_alias,6)