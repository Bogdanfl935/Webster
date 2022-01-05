#!/bin/bash

set -e # Exit if error occurs
set -u # Throw error if unset variables are used

function config_user_data() {
	local user=$(echo $1 | tr ':' ' ' | awk  '{print $1}')
	local password=$(echo $1 | tr ':' ' ' | awk  '{print $2}')
    echo "Creating user $user in database $POSTGRES_DB"
	psql -v ON_ERROR_STOP=1 -v user_var="$user"  -v password_var="$password" --username "$POSTGRES_USER" <<-EOSQL
		CREATE USER :user_var WITH ENCRYPTED PASSWORD ':password_var';
		GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO :user_var;
		GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO :user_var;
	EOSQL
}

if [ -n "$CREATE_USER_INTERACTIVE" -a "${CREATE_USER_INTERACTIVE,,}" = "on" ]
then
	echo "Interactive user active, awaiting <user:password> input"
    while IFS='$\n' read -r line; do
        config_user_data "$line"
    done
fi