-- :name set_privacy_access_relationship :insert
insert into granted_privacy_access (grantor_id, grantee_id) values (:grantor_id, :grantee_id)