"""
StudyChart AI - Analytics Engine Tests.
"""

def test_analytics_metrics(client):
    reg_data = {
        "name": "Analytics Student",
        "email": "analytics@studychart.ai",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    client.post("/api/v1/auth/register", json=reg_data)
    login_resp = client.post("/api/v1/auth/login", json={"email": "analytics@studychart.ai", "password": "Password123!"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Log two study sessions
    client.post("/api/v1/study-sessions", json={"duration_minutes": 30, "topic_title": "Trees"}, headers=headers)
    client.post("/api/v1/study-sessions", json={"duration_minutes": 45, "topic_title": "Graphs"}, headers=headers)

    analytics_resp = client.get("/api/v1/analytics", headers=headers)
    assert analytics_resp.status_code == 200
    data = analytics_resp.json()
    assert data["total_study_minutes"] >= 75
    assert len(data["daily_history"]) == 7
