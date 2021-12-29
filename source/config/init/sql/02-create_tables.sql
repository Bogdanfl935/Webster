\set TAG_MAX_LENGTH 1000
\set DESCRIPTION_MAX_LENGTH 60
\set KEYWORD_MAX_LENGTH 15


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
