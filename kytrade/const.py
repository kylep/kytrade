"""Constants and environment variable checks"""
import os
import sys


def env_var(env_var_name, default, required=False):
    """Return an environment variable if it exists else a default"""
    if required and env_var_name not in os.environ:
        sys.stderr.write(f"ERROR: env var {env_var_name} is required\n")
        sys.exit(1)
    val = os.environ[env_var_name] if env_var_name in os.environ else default
    if str(val).upper() == "TRUE":
        val = True
    if str(val).upper() == "FALSE":
        val = False
    return val


VERSION = "1.0001"
# env_var allows reconfiguring the tool without config files - works well with containers too

# Upstream API Keys
# Currently *none* of these are required, Yahoo's data doesn't need an API key
ALPHAVANTAGE_API_KEY = env_var("ALPHAVANTAGE_API_KEY", None, required=False)
STOCKSHARK_API_KEY = env_var("STOCKSHARK_API_KEY", None, required=False)
ALPACA_API_KEY_ID = env_var("ALPACA_API_KEY_ID", None, required=False)
ALPACA_API_KEY_SECRET = env_var("ALPACA_API_KEY_SECRET", None, required=False)
ALPACA_API_ENDPOINT = env_var("ALPACA_API_ENDPOINT", "https://paper-api.alpaca.markets")
IEXCLOUD_API_KEY = env_var("IEXCLOUD_API_KEY", None, required=False)

# Database
SQLA_DRIVER = env_var("SQLA_DRIVER", "mysql")
SQLA_ECHO = env_var("SQLA_ECHO", False)
SQL_HOST = env_var("SQL_HOST", "127.0.0.1")
SQL_PORT = env_var("SQL_PORT", 3306)
SQL_USER = env_var("SQL_USER", "root")
SQL_PASS = env_var("SQL_PASS", None, required=True)
SQL_DATABASE = env_var("SQL_DATABASE", "trade")

# General settings
TX_BROKERAGE_COMISSION = float(env_var("TX_BROKERAGE_COMISSION", 10.00))
RISK_FREE_RATE = float(env_var("RISK_FREE_RETURN", 0.39))  # As of 2022-02-24
ADJUST_FOR_DIVIDENDS = env_var("ADJUST_FOR_DIVIDENDS", True)
