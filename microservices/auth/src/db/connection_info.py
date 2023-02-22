"""
    Database connection URL.

    Database connection URL used for connecting to database.
"""
from config.config import settings


SQL_ALCHEMY_MYSQL_CONNECTION_URL = url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
        settings.mysql_user, settings.mysql_root_password, 
        settings.mysql_host, settings.mysql_port, settings.mysql_database
    )
