"""
StudyChart AI - Subject and Unit Hierarchy Tests.
"""

def test_subject_unit_topic_hierarchy(client):
    reg_data = {
        "name": "David Miller",
        "email": "david@studychart.ai",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    client.post("/api/v1/auth/register", json=reg_data)
    login_resp = client.post("/api/v1/auth/login", json={"email": "david@studychart.ai", "password": "Password123!"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Subject
    subj_resp = client.post("/api/v1/subjects", json={
        "name": "Database Management Systems",
        "description": "Relational algebra, SQL, and indexing",
        "color": "#6366f1",
        "icon": "database",
        "priority": 4
    }, headers=headers)
    assert subj_resp.status_code == 201
    subj_id = subj_resp.json()["id"]

    # 2. Add Unit
    unit_resp = client.post(f"/api/v1/subjects/{subj_id}/units", json={
        "title": "Unit 1: Relational Schema & Normalization",
        "description": "1NF to BCNF and functional dependencies",
        "order_index": 1,
        "topics": [
            {
                "title": "First and Second Normal Form",
                "difficulty": 2.5,
                "estimated_minutes": 45,
                "order_index": 1
            },
            {
                "title": "Third Normal Form & BCNF",
                "difficulty": 4.0,
                "estimated_minutes": 60,
                "order_index": 2
            }
        ]
    }, headers=headers)
    assert unit_resp.status_code == 201

    # 3. Verify Full Subject Tree
    get_subj = client.get(f"/api/v1/subjects/{subj_id}", headers=headers)
    assert get_subj.status_code == 200
    subj_data = get_subj.json()
    assert len(subj_data["units"]) == 1
    assert len(subj_data["units"][0]["topics"]) == 2
    assert subj_data["total_topics"] == 2
