"""
    Helper class for hashing.

    This module is responsible for generating hasing for password and creating access token.
"""

from passlib.context import CryptContext
from config.config import settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """
    Get hashed password

    To generate hash for the password.

    Parameters
    ----------
    password : str
        Password of the user in plain format.

    Returns
    -------
    str
        Password of the user in hashed format.
    """
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    """
    Verify the provided password.

    The password entered by the user is checked against the hashed version of the same password.

    Parameters
    ----------
    password : str
        Password of the user in plain format.
    hashed_pass : str
        Password of the user in hashed format.

    Returns
    -------
    bool
        True if there is a match else False
    """
    return password_context.verify(password, hashed_pass)
