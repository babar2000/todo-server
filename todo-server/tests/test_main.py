from fastapi.testclient import TestClient
from app.main import todo_server

client = TestClient(app=todo_server)

def test_hello():
	greet: str = "Hi"
	assert greet == "Hi"

def test_fastapi_hello():
	response = client.get("/")
	assert response.json() == {"Greet": "Hello World"}