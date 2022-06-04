-- :name remove_privacy_access :affected
DELETE FROM granted_privacy_access WHERE grantor_id = :grantor_id AND grantee_id = :grantee_id;