from fastapi.testclient import TestClient
from main import app

def test_ask():
    client = TestClient(app)
    resp = client.post("/ask/", json={"repo": "facebook/react", "question": "What is this repo?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "citations" in data
