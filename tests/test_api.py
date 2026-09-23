from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "JOCKY",
    }


def test_investigation_endpoint():
    response = client.post(
        "/investigate",
        json={
            "host": "HOST01",
            "checks": [
                "PROCESSES",
                "NETWORK",
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["host"] == "HOST01"
    assert data["platform"] == "Windows"
    assert data["evidence_records"] == 2
    assert isinstance(data["findings"], list)

    for finding in data["findings"]:
        assert finding["host"] == "HOST01"
        assert "category" in finding
        assert "severity" in finding
        assert "title" in finding
        assert "description" in finding
        assert "evidence" in finding


def test_investigation_requires_host():
    response = client.post(
        "/investigate",
        json={
            "checks": ["PROCESSES"],
        },
    )

    assert response.status_code == 422