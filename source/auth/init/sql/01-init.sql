--=========================================[MISC DDL]==========================================
CREATE EXTENSION citext;
CREATE DOMAIN email AS citext
	CHECK ( value ~ '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$' );

--=========================================[TABLE DDL]=========================================
CREATE TABLE App_User(
--	Field name						Field type			Field constraints
	id 								BIGINT 		PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	username 						EMAIL 		UNIQUE NOT NULL,
	password 						TEXT 		NOT NULL,
	is_enabled						BOOLEAN		NOT NULL,
	is_credentials_non_expired		BOOLEAN		NOT NULL
);

CREATE VIEW User_Record AS SELECT id, username FROM App_User;

CREATE TABLE Role(
--	Field name		Field type			Field constraints
	id 				BIGINT 		PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	title 			CITEXT 		UNIQUE NOT NULL
);

CREATE TABLE App_User_Role(
--	Field name		Field type			Field constraints
	app_user_id 	BIGINT 		REFERENCES App_User,
	role_id 		BIGINT 		REFERENCES Role,
	PRIMARY KEY(app_user_id, role_id)
);