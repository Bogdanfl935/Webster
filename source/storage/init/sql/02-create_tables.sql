\set URL_MAX_LENGTH 2048
\set TAG_MAX_LENGTH 1000
\set EXTENSION_MAX_LENGTH 256
\set DESCRIPTION_MAX_LENGTH 60
\set KEYWORD_MAX_LENGTH 15

-- Creation of parsed url table
CREATE TABLE parsed_url (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  url VARCHAR(:URL_MAX_LENGTH) NOT NULL
);

-- Creation of visited url table
CREATE TABLE visited_url (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  url VARCHAR(:URL_MAX_LENGTH) NOT NULL
);

-- Creation of parser configuration table
CREATE TABLE parser_configuration (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  tag VARCHAR(:TAG_MAX_LENGTH) NOT NULL,
  UNIQUE(user_id, tag)
);

-- Creation of crawler option table
CREATE TABLE crawler_option (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  keyword VARCHAR(:KEYWORD_MAX_LENGTH) NOT NULL UNIQUE,
  description VARCHAR(:DESCRIPTION_MAX_LENGTH) NOT NULL
);

-- Creation of crawler configuration table
CREATE TABLE crawler_configuration (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  option_id INT NOT NULL REFERENCES crawler_option,
  UNIQUE(user_id, option_id)
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
  content bytea NOT NULL
);

-- Creation of parsed image table
CREATE TABLE parsed_image (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL,
  extension VARCHAR(:EXTENSION_MAX_LENGTH) NOT NULL,
  content bytea NOT NULL
);
