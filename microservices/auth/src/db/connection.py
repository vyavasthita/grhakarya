"""
    Database connection.

    This module is responsible for database connection.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.connection_info import SQL_ALCHEMY_MYSQL_CONNECTION_URL as connection_url


engine = create_engine(url=connection_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

