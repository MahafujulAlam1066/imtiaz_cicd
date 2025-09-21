from fastapi.testclient import TestClient
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sourcecode")))

from performance_test import api  # Import your FastAPI app

client = TestClient(api)



def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Book Management System"}


def test_add_book():
    book = {
        "id": 1,
        "name": "Python Basics",
        "description": "Intro to Python",
        "isAvailable": True
    }
    response = client.post("/book", json=book)
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Python Basics"


def test_get_books():
    response = client.get("/book")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_book():
    updated_book = {
        "id": 1,
        "name": "Python Advanced",
        "description": "Deep dive into Python",
        "isAvailable": False
    }
    response = client.put("/book/1", json=updated_book)
    assert response.status_code == 200
    assert response.json()["name"] == "Python Advanced"


def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1



def test_update_nonexistent_book():
    updated_book = {
        "id": 999,
        "name": "Nonexistent",
        "description": "No book here",
        "isAvailable": True
    }
    response = client.put("/book/999", json=updated_book)
    assert response.status_code == 200
    assert response.json() == {"error": "Book Not Found"}


def test_delete_nonexistent_book():
    response = client.delete("/book/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Book not found, deletion failed"}
