from fastapi.testclient import TestClient
from main import app

def test_repos():
    client = TestClient(app)
    resp = client.get("/repos/")
    assert resp.status_code == 200
    data = resp.json()
    assert "repos" in data
