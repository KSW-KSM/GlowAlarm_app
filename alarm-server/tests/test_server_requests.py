import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000" 

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check Response:", response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_set_alarm():
    data = {
        "alarm_time": "08:00",
        "bed_time": "23:00",
        "wake_up_time": "07:00"
    }
    response = requests.post(f"{BASE_URL}/set_alarm", json=data)
    print("Set Alarm Response:", response.json())
    assert response.status_code == 200
    assert "optimal_time" in response.json()

def test_stop_alarm():
    response = requests.post(f"{BASE_URL}/stop_alarm")
    print("Stop Alarm Response:", response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Alarm stopped"

def test_snooze_alarm():
    set_alarm_data = {
        "alarm_time": "07:30",
        "bed_time": "23:00",
        "wake_up_time": "07:00"
    }
    requests.post(f"{BASE_URL}/set_alarm", json=set_alarm_data)

    # 현재 시간을 알람 시간으로 가정하고 5분 스누즈
    current_time = datetime.now().strftime("%H:%M")
    snooze_data = {
        "current_time": current_time,
        "snooze_duration": 5
    }
    response = requests.post(f"{BASE_URL}/snooze_alarm", json=snooze_data)
    print("Snooze Alarm Response:", response.json())
    assert response.status_code == 200
    assert "new_alarm_time" in response.json()

def test_get_alarms():
    response = requests.get(f"{BASE_URL}/alarms")
    print("Get Alarms Response:", json.dumps(response.json(), indent=2))
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

if __name__ == "__main__":
    print("Testing Health Check")
    test_health_check()
    print("\nTesting Set Alarm")
    test_set_alarm()
    print("\nTesting Stop Alarm")
    test_stop_alarm()
    print("\nTesting Snooze Alarm")
    test_snooze_alarm()
    print("\nTesting Get Alarms")
    test_get_alarms()
    print("\nAll tests completed.")