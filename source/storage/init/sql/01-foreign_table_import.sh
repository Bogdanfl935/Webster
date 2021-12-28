#!/bin/bash

set -e # Exit if error occurs
set -u # Throw error if unset variables are used

function import_foreign_table() {
    echo "Importing table $REMOTE_DB_TABLENAME from $REMOTE_DB_DATABASE"
	psql -v ON_ERROR_STOP=1 \
        -v remote_username="$REMOTE_DB_USERNAME"  -v remote_password="$REMOTE_DB_PASSWORD" \
        -v remote_database="$REMOTE_DB_DATABASE" -v remote_host="$REMOTE_DB_HOST" -v remote_port="$REMOTE_DB_PORT" \
        -v remote_tablename="$REMOTE_DB_TABLENAME" --username "$POSTGRES_USER" <<-EOSQL
		CREATE EXTENSION postgres_fdw;
        CREATE EXTENSION citext;
        CREATE DOMAIN email AS citext;
        CREATE SERVER remote_pg_server FOREIGN DATA WRAPPER postgres_fdw
        OPTIONS (dbname :'remote_database', host :'remote_host', port :'remote_port');

        CREATE USER MAPPING FOR CURRENT_USER SERVER remote_pg_server OPTIONS (user :'remote_username', password :'remote_password');

        IMPORT FOREIGN SCHEMA "public" limit to (:remote_tablename) FROM SERVER remote_pg_server INTO public;
	EOSQL
}

if [ -n "$REMOTE_DB_HOST" -a        \
    -n "$REMOTE_DB_PORT" -a         \
    -n "$REMOTE_DB_DATABASE" -a     \
    -n "$REMOTE_DB_TABLENAME" -a    \
    -n "$REMOTE_DB_USERNAME" -a     \
    -n "$REMOTE_DB_PASSWORD" ]
then
	import_foreign_table
fi