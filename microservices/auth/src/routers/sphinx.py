from starlette.routing import Mount, BaseRoute
from starlette.staticfiles import StaticFiles
from typing import List
from config.config import settings


def sphinx_routes() -> List[BaseRoute]:
    """
    Sphinx static routes

    Provide a list of static routes to add when initializing app

    Returns
    -------
    List[BaseRoute]
        List of routes
    """
    sphinx = Mount(
                path="/docs",
                app=StaticFiles(directory=settings.sphinx_directory, html=True),                  
                name="sphinx"
            )
    return [sphinx]