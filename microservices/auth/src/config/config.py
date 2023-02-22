"""
    Setting Module

    Environment variable based configuration module.
"""

from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    """
    Configuration Class.

    Configuration for auth API.
    All variables in class corresponds to environment variables in CAPITAL CASE.
    example: 'mysql_host' represents an environment variable by name 'MYSQL_HOST'.

    Parameters
    ----------
    BaseSettings : BaseSettings.
        Base Class for Settings
    """
    environment:str = "development"
    api_version:str = None
    api_title:str = None
    api_host:str = None
    api_port:int = None
    sphinx_directory:str = None

    log_config:str = None
    log_file_path:str = None
    log_file_name:str = None

    mysql_host:str = None
    mysql_port:str = None
    mysql_database:str = None
    mysql_user: str = None
    mysql_root_password: str = None

    secret_key: str = None
    algorithm: str = None
    access_token_expire_minutes: int = None


settings = Settings()
