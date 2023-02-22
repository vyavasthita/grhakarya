"""
    OAuth2 connection.

    This module is responsible for providing authorization using password flow.
    'tokenURL' represents an endpoint.

    Whenenver user is asked for authorization and when user enters username and password
    and submits then requests is forwarded to endpoint given in 'tokenUrl'.
"""
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/login")
