#!/bin/bash
echo "WARNING: This will delete all the data"
echo "To continue, enter: y"
read -r verify
if [[ "$verify" != "y" ]]; then
  exit 0
fi

echo "Dropping the database"
docker exec -it kytrade-sql mysql -u root -p$SQL_PASS -e "DROP DATABASE trade;"
docker exec -it kytrade-sql mysql -u root -p$SQL_PASS -e "CREATE DATABASE trade;"

kt init database-tables

echo
echo "Downloading some stock data"
for ticker in SPY QQQ AAPL; do
kt download daily-stock-prices $ticker
sleep 12  # Alphavantage free has a 5 calls/minute limit
done


