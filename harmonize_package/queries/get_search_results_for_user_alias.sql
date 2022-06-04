-- :name get_search_results_for_user_alias :many
SELECT public.user.id, public.user.user_alias, public.user.user_type FROM public.user
WHERE
    LEFT(user_alias,3) = LEFT(:user_alias,3)
   OR
    RIGHT(user_alias,4) = RIGHT(:user_alias,4)
   OR
    LEFT(user_alias,6) = LEFT(:user_alias,6)
   OR
    RIGHT(user_alias,6) = RIGHT(:user_alias,6)