"""Stock Shark API"""
import requests
import json

from kytrade.const import STOCKSHARK_API_KEY

# Reference:
# https://studio-ws.apicur.io/sharing/858eb68a-9f2c-4655-aeee-7bf8a8c336fa

url = f"https://stock-shark.com/api/v1/searchTicker?ticker=SPY&token={STOCKSHARK_API_KEY}"
url = f"https://stock-shark.com/api/v1/getHistoricalPrice?periodType=daily&ticker=SPY&token={STOCKSHARK_API_KEY}"
x = requests.get(url)
data = json.loads(x.content)

# none of these work, 400 token errors
