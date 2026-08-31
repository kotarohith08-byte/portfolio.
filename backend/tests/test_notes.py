"""
StudyChart AI - Notes & AI Action Tests.
"""

def test_notes_crud_and_ai_action(client):
    reg_data = {
        "name": "Sarah Connor",
        "email": "sarah@studychart.ai",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    client.post("/api/v1/auth/register", json=reg_data)
    login_resp = client.post("/api/v1/auth/login", json={"email": "sarah@studychart.ai", "password": "Password123!"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Note
    note_resp = client.post("/api/v1/notes", json={
        "title": "SQL Indexing Techniques",
        "content": "B-Tree indexes allow O(log n) search on sorted columns. Hash indexes allow O(1) equality lookups.",
        "tags": "sql,indexing,database",
        "is_pinned": True
    }, headers=headers)
    assert note_resp.status_code == 201
    note_id = note_resp.json()["id"]

    # 2. AI Summarize Action
    ai_resp = client.post(f"/api/v1/notes/{note_id}/ai", json={"action": "summarize"}, headers=headers)
    assert ai_resp.status_code == 200
    assert "result" in ai_resp.json()

    # 3. Verify Note updated with summary
    get_note = client.get(f"/api/v1/notes/{note_id}", headers=headers)
    assert get_note.status_code == 200
    assert get_note.json()["ai_summary"] is not None
