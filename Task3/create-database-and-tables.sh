#!/bin/sh
echo "Creating table store..."
psql -h database -d $POSTGRES_DB -c \
'CREATE TABLE store (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL);'
echo "Showing created table store..."
psql -h database -d $POSTGRES_DB -c \
'\d store'