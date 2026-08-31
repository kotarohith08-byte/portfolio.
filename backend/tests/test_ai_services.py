"""
StudyChart AI - AI Orchestrator Tests.
"""

def test_ai_tutor_and_plan_generation(client):
    reg_data = {
        "name": "AI Tester",
        "email": "aitester@studychart.ai",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    client.post("/api/v1/auth/register", json=reg_data)
    login_resp = client.post("/api/v1/auth/login", json={"email": "aitester@studychart.ai", "password": "Password123!"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. AI Study Plan Generation
    plan_resp = client.post("/api/v1/ai/study-plan", json={
        "subject_names": ["Operating Systems", "Computer Networks"],
        "daily_hours": 3,
        "difficult_topics": ["Virtual Memory", "TCP Congestion Control"]
    }, headers=headers)
    assert plan_resp.status_code == 200
    plan_data = plan_resp.json()
    assert "schedule" in plan_data

    # 2. AI Tutor Message
    tutor_resp = client.post("/api/v1/ai/tutor", json={
        "message": "Explain recursion like I am a beginner."
    }, headers=headers)
    assert tutor_resp.status_code == 200
    tutor_data = tutor_resp.json()
    assert "message" in tutor_data
    assert len(tutor_data["message"]) > 0

    # 3. AI Performance Analysis
    perf_resp = client.post("/api/v1/ai/analyze-performance", headers=headers)
    assert perf_resp.status_code == 200
    assert "strengths" in perf_resp.json()
