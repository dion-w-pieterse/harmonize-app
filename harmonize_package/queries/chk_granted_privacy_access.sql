-- :name chk_granted_privacy_access :one
SELECT gpa.grantee_id
FROM granted_privacy_access AS gpa
WHERE gpa.grantor_id = :grantor_id
  AND gpa.grantee_id = :grantee_id;