"""
    Token schema.

    This represents the Token schema representing Access token for the user.
"""
from pydantic import BaseModel, Field
from typing import Union


class Token(BaseModel):
    access_token: str = Field(example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWxpcEBnbWFpbC5jb20iLCJleHAiOjE2NzUzMDE5ODh9.1Z_RbvIZpaV78wB2cio4nP3ZRysduT-NDYLa2wNENbI")
    token_type: str = Field(example="bearer")


class TokenData(BaseModel):
    username: Union[str, None] = Field(example="user@gmail.com")
