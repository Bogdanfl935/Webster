-- Creation of parsed_urls table
CREATE TABLE parsed_urls (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  url varchar(2083) NOT NULL
);

-- Creation of visited_urls table
CREATE TABLE visited_urls (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  url varchar(2083) NOT NULL
);

-- Creation of config table
CREATE TABLE config (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  key varchar(16) NOT NULL,
  value varchar(16) NOT NULL
);

-- Creation of parsed_content table
CREATE TABLE parsed_content (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  tag varchar(32) NOT NULL,
  content bytea NOT NULL
);

-- Creation of parsed_images table
CREATE TABLE parsed_images (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  extension varchar(16) NOT NULL,
  content bytea NOT NULL
);