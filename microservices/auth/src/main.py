"""
    Main module for API.

    This module is the main module for Fast API app.
"""
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.config import settings
from utils.file_helper import create_dir_if_not_exists


if settings.environment == 'development':
    create_dir_if_not_exists(settings.log_file_path)

from routers import token
from routers.sphinx import sphinx_routes


description = """
Auth Microservide for grahakarya project. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "token",
        "description": "To Create access token and to get authorization.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    title=settings.api_title,
    description=description,
    version=settings.api_version,
    openapi_tags=tags_metadata,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Dilip Kumar Sharma",
        "url": "https://www.linkedin.com/in/diliplakshya/",
        "email": "diliplakshya@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    redoc_url=None,
    docs_url="/client",
    routes=sphinx_routes(),
)

app.include_router(token.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def home():
    return {"Samskriti": "Samskar"}

if __name__ == '__main__':
    from db.connection import Base, engine
    Base.metadata.create_all(bind=engine)
        
    uvicorn.run("main:app", host=settings.api_host, port=settings.api_port, reload=True)
