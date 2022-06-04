-- :name set_last_login_date :affected
update public.user set last_login = CURRENT_TIMESTAMP at time zone 'utc'
where public.user.id = :user_id