import sys
from pathlib import Path

# Ensure src is importable
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Math Olympiad"
    email = "test_student@example.com"

    # Sign up
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert email in [p for p in client.get("/activities").json()[activity]["participants"]]

    # Duplicate signup should fail
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r2.status_code == 400

    # Unregister
    r3 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r3.status_code == 200
    assert email not in [p for p in client.get("/activities").json()[activity]["participants"]]


def test_signup_nonexistent_activity():
    r = client.post("/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    assert r.status_code == 404


def test_unregister_nonexistent_participant():
    r = client.delete("/activities/Chess Club/participants", params={"email": "nope@mergington.edu"})
    assert r.status_code == 404
