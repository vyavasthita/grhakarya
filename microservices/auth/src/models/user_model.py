"""
    User Data model.

    User data model representing User DB table.
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.connection import Base


class User(Base):
    """
    User Model Schema class.

    It represents User DB table in database.

    Parameters
    ----------
    Base : Base
        Base class for data model.
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30), unique=True, index=True)
    hashed_password = Column(String(60))
    is_active = Column(Boolean, default=True)
