"""
    DB dependency.

    This module is responsible for providing DB connection dependencies to other modules.
    It creates a DB connection session object and returns it to calling module.
"""
from db.connection import SessionLocal


# Get DB Connection Session
def db_session() -> SessionLocal:
    """
    Get DB session.

    To get Database connection session object.
    Session is closed when use of session object is over.

    Yields
    ------
    SessionLocal
        Session object used for executing database query.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


