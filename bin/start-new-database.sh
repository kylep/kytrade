#!/bin/bash
if [[ "$SQL_PASS" == "" ]]; then echo "ERROR: gotta set SQL_PASS"; exit 1; fi
if [[ ! -d bin || ! -d kytrade ]]; then echo "ERROR: run this in the base checkout dir"; exit 1; fi

mkdir -p db-data

# For Intel CPUs
# IMAGE="mysql:latest"

# For ARM CPUs
IMAGE="arm64v8/mysql:oracle"

docker run -d \
  -p 127.0.0.1:3306:3306 \
  --name kytrade-sql \
  --volume $(pwd)/db-data/:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=$SQL_PASS \
  -e MYSQL_PASS=$SQL_PASS \
  $IMAGE

delay=30
echo "waiting $delay seconds for db to init"
sleep $delay

echo "...creating database"
docker exec -it kytrade-sql mysql -u root -p$SQL_PASS -e "CREATE DATABASE trade;"
