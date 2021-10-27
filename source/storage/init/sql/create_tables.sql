-- Creation of next_links table
CREATE TABLE next_links (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  url_site varchar(2083) NOT NULL
);

-- Creation of visited_links table
-- CREATE TABLE IF NOT EXISTS visited_links (
--   link_id SERIAL,
--   url_site varchar(2083) NOT NULL,
--   PRIMARY KEY (link_id)
-- );