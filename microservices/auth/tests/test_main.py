from fastapi.testclient import TestClient
from fastapi import status
import os, sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__name__), 'src')))

from ..src.main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Samskriti": "Samskar"}
