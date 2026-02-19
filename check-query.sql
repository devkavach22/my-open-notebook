SELECT id, title, 
  CASE 
    WHEN full_text IS NULL THEN 'NULL'
    WHEN full_text = '' THEN 'EMPTY'
    ELSE string::slice(full_text, 0, 100)
  END AS full_text_preview,
  string::len(full_text) AS text_length
FROM source;
