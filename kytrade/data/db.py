"""Database Functions"""
import sqlalchemy
from sqlalchemy.orm import Session
from pandas.core.frame import DataFrame

from kytrade import const
from kytrade.data import models


# future=False because pandas does not support 2.0 with to_sql yet
# https://github.com/pandas-dev/pandas/issues/40460
engine = sqlalchemy.create_engine(
    (
        f"{const.SQLA_DRIVER}://"
        f"{const.SQL_USER}:{const.SQL_PASS}"
        f"@{const.SQL_HOST}:{const.SQL_PORT}"
        f"/{const.SQL_DATABASE}"
    ),
    echo=const.SQLA_ECHO,
    future=False,
)


def init_create_tables():
    """Create the ORM-defined tables"""
    models.Base.metadata.create_all(engine)


def get_session() -> Session:
    """Get a session for this engine"""
    return Session(engine)


def save_dataframe(orm_model: models.Base, df: DataFrame) -> None:
    """Save a pandas dataframe to the db as a given model"""
    df.to_sql(
        orm_model.__tablename__,
        schema=const.SQL_DATABASE,
        con=engine,
        index=False,
        if_exists="append",
        method="multi",
    )
