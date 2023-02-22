"""
    Logging module.

    This module is responsible for providing logging service to all modules.
"""
import os
import logging
from logging import config
from config.config import settings


class AuthFileLogger():
    """
    Logging Wrapper class.

    This class is a wrapper class on the top of Logging module.
    This is used for providing single class across all other modules.
    """
    # The config file for logging formatter.
    if settings.environment == "development":
        config.fileConfig(settings.log_config, defaults={"logfile": os.path.join(settings.log_file_path, settings.log_file_name)}, disable_existing_loggers=True)
    else:
        config.fileConfig(settings.log_config, disable_existing_loggers=True)

    def __init__(self, name) -> None:
        """
        Initialization for Logging wrapper class.

        This initializes logger for a given module.

        Parameters
        ----------
        name : str
            Name of the module which is going to use this class for logging.
        """
        self.logger=logging.getLogger(name)

    def log_debug(self, message) -> None:
        """
        To log Debug.

        To log messages for DEBUG level.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self.logger.debug(message)

    def log_info(self, message) -> None:
        """
        To log Info.

        To log messages for INFO level.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self.logger.info(message)

    def log_warning(self, message) -> None:
        """
        To log Warning.

        To log messages for WARNING level.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self.logger.warning(message)

    def log_error(self, message) -> None:
        """
        To log error.

        To log messages for ERROR level.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self.logger.error(message)

    def log_critical(self, message) -> None:
        """
        To log Critical.

        To log messages for CRITICAL level.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self.logger.critical(message)