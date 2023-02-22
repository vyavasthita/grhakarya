"""
    DAO for user.

    Data Access Object for User data model.
    This module is responsible for accessing database tables.
 """
from fastapi import Depends
from sqlalchemy.orm import Session
from models import user_model
from schemas.user_schema import UserCreate, User


def get_user(db: Session, user_id: int) -> User:
    """
    Retrieve User from DB.

    To retrieve user from User table from database based on user_id.

    Parameters
    ----------
    db : Session
        Database connection session object.
    user_id : int
        Unique id for each user in User DB table.

    Returns
    -------
    User
        User data model representing User DB table.
    """
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User:
    """
    Get User from DB.

    Get User from DB table based on email.

    Parameters
    ----------
    db : Session
        Database connection session object.
    email : str
        Email ID of the user

    Returns
    -------
    User
        User data model representing User DB table.
    """
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create new User.

    Create new User in DB table.

    Parameters
    ----------
    db : Session
        Database connection session object.
    user : UserCreate
        New user attributes like email id and hashed password.

    Returns
    -------
    User
        User data model representing User DB table.
    """
    db_user = user_model.User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
