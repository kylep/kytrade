#!/bin/bash
if [[ "$SQL_PASS" == "" ]]; then echo "ERROR: gotta set SQL_PASS"; exit 1; fi
if [[ ! -d bin || ! -d kytrade ]]; then echo "ERROR: run this in the base checkout dir"; exit 1; fi

# db data gets saved to database/, it's already in .gitignore
mkdir -p db-data


# NOTE: I tried postgresql but it was just way too slow

docker run -d \
  -p 127.0.0.1:3306:3306 \
  --name kytrade-sql \
  --volume $(pwd)/db-data/:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=$SQL_PASS \
  -e MYSQL_PASS=$SQL_PASS \
  mysql:latest

# docker exec -u postgres -it trade-sql bash

delay=30
echo "waiting $delay seconds for db to init"
sleep $delay

echo "...creating database"
docker exec -it kytrade-sql \
  mysql -u root -p$SQL_PASS -e "CREATE DATABASE trade;"


# TODO: Remove this - pretty sure sqla will do it now
#echo "...creating prices_day table"
#sleep 1
#docker exec -it trade-sql \
#  mysql -u root -p$SQL_PASS trade -e "CREATE TABLE prices_day (ticker varchar(8), date DATE, open FLOAT, high FLOAT, low FLOAT, close FLOAT, volume FLOAT);"

#echo "...creating sma table"
#sleep 1
#docker exec -it trade-sql \
#  mysql -u root -p$SQL_PASS trade -e "CREATE TABLE sma (ticker varchar(8), date DATE, style VARCHAR(16), days INT, value FLOAT);"
