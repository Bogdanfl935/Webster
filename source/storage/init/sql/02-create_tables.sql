\set URL_MAX_LENGTH 2048
\set TAG_MAX_LENGTH 1000
\set EXTENSION_MAX_LENGTH 256
\set DESCRIPTION_MAX_LENGTH 60
\set KEYWORD_MAX_LENGTH 15

CREATE TYPE URL_STATE AS ENUM ('READY', 'PENDING', 'VISITED');

-- Creation of parsed url table
CREATE TABLE parsed_url (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  url VARCHAR(:URL_MAX_LENGTH) NOT NULL,
  state URL_STATE NOT NULL,
  UNIQUE(user_id, url)
);

-- Creation of memory usage table
CREATE TABLE memory_usage (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL UNIQUE,
  usage BIGINT NOT NULL CHECK (usage > 0)
);

-- Creation of memory limit table
CREATE TABLE memory_limit (
  singleton_key bool PRIMARY KEY DEFAULT TRUE CHECK (singleton_key),
  capacity BIGINT NOT NULL CHECK (capacity > 0)
);

-- Creation of parsed content table
CREATE TABLE parsed_content (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  tag VARCHAR(:TAG_MAX_LENGTH) NOT NULL,
  content bytea NOT NULL,
  source_id BIGINT NOT NULL REFERENCES parsed_url
);

-- Creation of parsed image table
CREATE TABLE parsed_image (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  extension VARCHAR(:EXTENSION_MAX_LENGTH) NOT NULL,
  content bytea NOT NULL,
  source_id BIGINT NOT NULL REFERENCES parsed_url
);
