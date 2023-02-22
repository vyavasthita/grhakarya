"""
    Service class for authentication.

    This represents the business logic for authentication.
"""

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt
from datetime import datetime, timedelta
from typing import Union
from dao.user_dao import get_user_by_email, create_user
from utils.hashing_helper import get_hashed_password, verify_password
from dependencies.db_dependency import db_session
from dependencies.oauth_dependency import oauth2_scheme
from config.config import settings
from schemas.user_schema import User, UserCreate


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Create access token

    To create access token for a given user using JWT.

    Parameters
    ----------
    data : dict
        User data for which access token to be created.
    expires_delta : Union[timedelta, None]
        Expiry time after which generated access token will be expired.

    Returns
    -------
    str
        Hashed access token using JWT.
    """
    to_encode = data.copy()

    if not expires_delta:
        expires_delta = timedelta(minutes=5)

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def generate_access_token(username: str) -> str:
    """
    Generate access token.

    To generate access token for a given user using JWT.

    Parameters
    ----------
    username : str
        To user for which access token to be generated.

    Returns
    -------
    str
        Hashed access token using JWT.
    """
    return create_access_token(
        data={"sub": username}, expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )

def create_new_user(db: Session, user: UserCreate) -> User:
    """
    To create new user.

    To create new user in database.
    This method calls DAO which is responsible for executing DB query.

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

    Raises
    ------
    HTTPException
        For duplicate user.
    """
    if get_user_by_email(db=db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate user.",
        )

    user.password = get_hashed_password(user.password)
    return create_user(db=db, user=user)


def authenticate_user(db: Session, email: str, password: str) -> User | bool:
    """
    To authenticate given user.

    This method talks with DAO module to check if the given user is a registered user.

    Parameters
    ----------
    db : Session
        Database connection session object.
    email : str
        Email id of the user for which authentication has to be checked.
    password : str
        Password of the user for which authentication has to be checked.

    Returns
    -------
    User | bool
        User: If user is authenticated then it returns User data model representing User DB table.
        bool: If user is not authenticated then it returns False.
    """
    user = get_user_by_email(db=db, email=email)
    return False if not user or not verify_password(password, get_hashed_password(password)) else user

async def decode_token(token: str = Depends(oauth2_scheme)) -> str | None:
    """
    To decode access token.

    This methods decodes the access token of the currently activated user.
    It depends on 'oauth2_scheme' to get the access token of currently logged in user.

    It then decodes this access token using JWT by using Secret key.

    Once it is decoded then username is fetched from the access token details.

    Parameters
    ----------
    token : str
        Access token of currently logged in user.

    Returns
    -------
    str | None
        str: If decoding is done successfully then username is fetched from decoded data.
        None: If exception is raised while decoding the access token.

    Raises
    ------
    HTTPException
        To represent the exception raised while decoding the access token.
    """
    username = None
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
    except JWTError:
        raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to validate credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

    return username

async def get_current_user(username: str = Depends(decode_token), db: Session = Depends(db_session)) -> User:
    """
    To get currently logged in user.

    This methods retrieves the username from the decoded access token data.

    Then it reads the username from DB to verify it is already registed user.

    Parameters
    ----------
    username : str
        The username fetched from the decoded access token.
    db : Session
        Database connection session object.

    Returns
    -------
    User
        User attributes like email id and hashed password fetched from DB.

    Raises
    ------
    HTTPException
        If user is not authenticated.

    HTTPException
        If user is not found in DB.
    """
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authticated.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(db=db, email=username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid User. User is not found in the server.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    To check the currently activated user.

    Once currently logged in user is successfully fetched, we check the user is active or not
    based on the attributes present in DB table for the given user.

    Parameters
    ----------
    current_user : User
        Currently logged in user.

    Returns
    -------
    User
        Currently logged in user.

    Raises
    ------
    HTTPException
        If user is not active.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return current_user