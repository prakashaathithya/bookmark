from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_health():
    assert client.get("/health").json() == {"status": "ok"}