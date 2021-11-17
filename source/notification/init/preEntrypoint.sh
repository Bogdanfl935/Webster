#!/bin/sh 

set -e
set -u

#Make sure all environment variables are set before executing main script

( : $SESSION_HOST )
( : $SESSION_PORT )
( : $SESSION_USER )
( : $SESSION_PASS )

exec "$@"