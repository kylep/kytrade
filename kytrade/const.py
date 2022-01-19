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
ALPHAVANTAGE_API_KEY = env_var("ALPHAVANTAGE_API_KEY", None, required=True)
SQLA_DRIVER = env_var("SQLA_DRIVER", "mysql")
SQLA_ECHO = env_var("SQLA_ECHO", False)
SQL_HOST = env_var("SQL_HOST","127.0.0.1")
SQL_PORT = env_var("SQL_PORT", 3306)
SQL_USER = env_var("SQL_USER", "root")
SQL_PASS = env_var("SQL_PASS", None, required=True)
SQL_DATABASE = env_var("SQL_DATABASE", "trade")
