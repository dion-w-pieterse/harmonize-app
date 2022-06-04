-- :name un_monitor_user :affected
DELETE FROM monitor WHERE monitor_id = :monitor_id AND monitoree_id = :monitoree_id;