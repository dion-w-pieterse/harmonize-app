-- :name chk_if_monitoring_user :one
SELECT m.monitoree_id
FROM monitor AS m
WHERE m.monitor_id = :monitor_id
AND m.monitoree_id = :monitoree_id;