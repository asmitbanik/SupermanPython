from fastapi.testclient import TestClient
from main import app

def test_index():
    client = TestClient(app)
    resp = client.post("/index/", json={"repo": "facebook/react"})
    assert resp.status_code == 200
    data = resp.json()
    assert "repo" in data
    assert "indexed" in data
    assert "updated" in data
    assert "head" in data
