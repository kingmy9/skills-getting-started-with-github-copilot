import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)
_original = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(_original))
    yield


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_and_unregister():
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]

    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_duplicate_signup_rejected():
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400


def test_unknown_activity():
    response = client.post("/activities/Nope/signup?email=a@mergington.edu")
    assert response.status_code == 404


def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess Club/unregister?email=ghost@mergington.edu")
    assert response.status_code == 400
