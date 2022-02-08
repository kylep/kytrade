from setuptools import setup

setup(
    name="kytrade",
    version="1.0",
    packages=["kytrade"],
    include_package_data=True,
    install_requires=[
        "sqlalchemy",
        "mysqlclient",
        "psycopg2-binary",
        "pandas",
        "numpy",
        "torch",
        "matplotlib",
        "alpha_vantage",
        "Click",
        "beautifultable",
        "gmpy2",
        "ib_insync"
    ],
    entry_points={"console_scripts": ["kt = kytrade.cli.main:shell"]},
)
