#!/bin/sh
echo "Creating database store..."
psql -h database -d $POSTGRES_DB -c \
'CREATE TABLE store (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL);'
echo "Showing created database store..."
psql -h database -d $POSTGRES_DB -c \
'\d store'