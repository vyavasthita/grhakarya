"""
    File related helper module

    This module provides method related to file and path
"""
import os


def create_dir_if_not_exists(path: str) -> bool:
    """
    Create dir path

    # Create directory & all intermediate directories if don't exists

    Parameters
    ----------
    path : str
        Directory & all intermediate directories path

    Returns
    -------
    bool
        Success or failure of creating dir
    """
    # Create target directory & all intermediate directories if don't exists
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory {path} created.")
    else:    
        print(f"Skipped creating directory {path}. Given directory already exists.")