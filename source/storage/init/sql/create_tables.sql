-- Creation of next_links table
CREATE TABLE next_links (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  url_site varchar(2083) NOT NULL
);

-- Creation of visited_links table
CREATE TABLE visited_links (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  url_site varchar(2083) NOT NULL
);

-- Creation of config table
CREATE TABLE config (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  key varchar(16) NOT NULL,
  value varchar(16) NOT NULL
);