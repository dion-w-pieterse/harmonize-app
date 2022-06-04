-- :name psql_fts :many
SELECT post.title AS post_title, post.body AS post_body
FROM post
WHERE to_tsvector(title || ' ' || body) @@ websearch_to_tsquery('english', :search_string);