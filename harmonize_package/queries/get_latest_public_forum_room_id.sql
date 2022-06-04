-- :name get_latest_public_forum_room_id :scalar
select max(id) from forum_room;