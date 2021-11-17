#!/bin/sh 

set -e
set -u

# Make sure all environment variables are set before executing main script
# IMPORTANT: Set EOL Conversion to Unix LF to fix the "File not found" error

( : $DB_HOSTNAME )
( : $DB_PORT )
( : $DB_DATABASE )
( : $DB_USER )
( : $DB_PASS )

( : $JEDIS_HOSTNAME )
( : $JEDIS_PORT )
( : $JEDIS_DATABASE )
( : $JEDIS_PASS )

( : $JWT_ISSUER )

exec "$@"