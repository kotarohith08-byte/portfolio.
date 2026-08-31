"""
StudyChart AI - Study Session and Pomodoro Timer Tests.
"""

def test_study_session_logging(client):
    reg_data = {
        "name": "Timer Tester",
        "email": "timertester@studychart.ai",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    client.post("/api/v1/auth/register", json=reg_data)
    login_resp = client.post("/api/v1/auth/login", json={"email": "timertester@studychart.ai", "password": "Password123!"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Log Session
    sess_resp = client.post("/api/v1/study-sessions", json={
        "topic_title": "Dynamic Programming (Knapsack & DAGs)",
        "duration_minutes": 50,
        "session_type": "pomodoro",
        "notes": "Solved 3 practice problems.",
        "productivity_rating": 5
    }, headers=headers)
    assert sess_resp.status_code == 201
    sess_data = sess_resp.json()
    assert sess_data["duration_minutes"] == 50
    assert sess_data["xp_earned"] == 75

    # 2. Check Dashboard reflect session
    dash_resp = client.get("/api/v1/dashboard", headers=headers)
    assert dash_resp.status_code == 200
    dash_data = dash_resp.json()
    assert dash_data["today_completed_minutes"] >= 50
