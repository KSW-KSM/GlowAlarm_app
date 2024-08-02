from fastapi.testclient import TestClient
from app.main import app
import pytest
from unittest.mock import patch

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch("app.utils.get_optimal_alarm_time")
def test_set_alarm_success(mock_get_optimal_alarm_time):
    mock_get_optimal_alarm_time.return_value = "06:45"

    response = client.post(
        "/set_alarm",
        json={"alarm_time": "08:00", "bed_time": "23:00", "wake_up_time": "07:00"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Alarm set successfully", "optimal_time": "06:45"}
@patch("app.utils.get_optimal_alarm_time")
async def test_set_alarm_failure(mock_get_optimal_alarm_time):
    mock_get_optimal_alarm_time.side_effect = Exception("API Error")

    response = await client.post(
        "/set_alarm",
        json={"alarm_time": "08:00", "bed_time": "23:00", "wake_up_time": "07:00"}
    )

    assert response.status_code == 500
    assert "API Error" in response.json()["detail"]

@patch("app.utils.snooze_alarm")
async def test_snooze_alarm_no_active_alarm(mock_snooze_alarm):
    mock_snooze_alarm.side_effect = ValueError("No active alarm found")

    response = await client.post(
        "/snooze_alarm",
        json={"current_time": "12:00", "snooze_duration": 5}
    )
    assert response.status_code == 404
    assert "No active alarm found" in response.json()["detail"]

def test_stop_alarm():
    response = client.post("/stop_alarm")
    assert response.status_code == 200
    assert response.json() == {"message": "Alarm stopped"}

@patch("app.utils.snooze_alarm")
def test_snooze_alarm(mock_snooze_alarm):
    mock_snooze_alarm.return_value = "07:35"

    response = client.post(
        "/snooze_alarm",
        json={"current_time": "07:30", "snooze_duration": 5}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Alarm snoozed for 5 minutes", "new_alarm_time": "07:35"}

def test_get_alarms():
    response = client.get("/alarms")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)