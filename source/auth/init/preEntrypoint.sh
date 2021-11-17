#!/bin/sh 

set -e
set -u

#Make sure all environment variables are set before executing main script

( : $DB_HOSTNAME )
( : $DB_PORT )
( : $DB_DATABASE )
( : $DB_USER )
( : $DB_PASS )

( : $JEDIS_HOSTNAME )
( : $JEDIS_PORT )
( : $JEDIS_DATABASE )
( : $JEDIS_PASS )

exec "$@"