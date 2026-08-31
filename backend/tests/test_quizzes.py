"""
StudyChart AI - Quiz Generation and Attempt Tests.
"""

def test_quiz_generation_and_scoring(client):
    reg_data = {
        "name": "Quiz Tester",
        "email": "quiztester@studychart.ai",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    client.post("/api/v1/auth/register", json=reg_data)
    login_resp = client.post("/api/v1/auth/login", json={"email": "quiztester@studychart.ai", "password": "Password123!"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. AI Quiz Generation
    gen_resp = client.post("/api/v1/ai/quiz", json={
        "topic": "SQL Joins and Aggregations",
        "difficulty": "intermediate",
        "number_of_questions": 3,
        "question_type": "mcq"
    }, headers=headers)
    assert gen_resp.status_code == 200
    quiz_data = gen_resp.json()
    assert len(quiz_data["questions"]) > 0
    quiz_id = quiz_data["id"]

    # 2. Submit Quiz Attempt
    first_q_id = quiz_data["questions"][0]["id"]
    attempt_resp = client.post(f"/api/v1/quizzes/{quiz_id}/attempt", json={
        "time_taken_seconds": 45,
        "answers": [
            {
                "question_id": first_q_id,
                "user_answer": "Optimal resource allocation and modular state encapsulation in SQL Joins and Aggregations"
            }
        ]
    }, headers=headers)
    assert attempt_resp.status_code == 200
    att_data = attempt_resp.json()
    assert "score" in att_data
    assert "xp_earned" in att_data
