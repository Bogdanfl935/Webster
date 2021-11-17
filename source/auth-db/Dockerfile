FROM postgres

# Environment variable CREATE_USER_INTERACTIVE can be set to add additional users to the configured database
# Format in terminal:
# user_1:password_1
# user_2:password_2
ENV CREATE_USER_INTERACTIVE="off"

COPY init/*.sql /docker-entrypoint-initdb.d/
COPY init/*.sh /docker-entrypoint-initdb.d/