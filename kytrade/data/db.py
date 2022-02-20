"""Database Functions"""
import sqlalchemy
from sqlalchemy.orm import Session
from pandas.core.frame import DataFrame
from sqlalchemy.orm.attributes import flag_modified

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
    return Session(bind=engine, expire_on_commit=False)


def save_dataframe(orm_model: models.Base, df: DataFrame) -> None:
    """Save a pandas dataframe to the db as a given model"""
    # TODO: Deprecate - not using pandas any more
    df.to_sql(
        orm_model.__tablename__,
        schema=const.SQL_DATABASE,
        con=engine,
        index=False,
        if_exists="append",
        method="multi",
    )


def commit(orm_object):
    """Commit an ORM object"""
    session = Session.object_session(orm_object)
    if not session:
        session = get_session()
        session.add(orm_object)
    session.commit()


def delete(orm_object):
    """Delete an ORM object"""
    session = Session.object_session(orm_object)
    session.delete(orm_object)
    session.commit()


def get_document(name: str) -> dict:
    """Get a document's data else {}"""
    query = sqlalchemy.select(models.Document).where(models.Document.name == name)
    session = get_session()
    result = session.execute(query).one_or_none()
    if result:
        return result[0].data
    return {}


def set_document(name: str, data: dict) -> None:
    """Write a document's data"""
    session = get_session()
    select_query = sqlalchemy.select(models.Document).where(models.Document.name == name)
    select_result = session.execute(select_query).one_or_none()
    if select_result:
        document = select_result[0]
        document.data = data
    else:
        document = models.Document(name=name, data=data)
    session.add(document)
    session.commit()

