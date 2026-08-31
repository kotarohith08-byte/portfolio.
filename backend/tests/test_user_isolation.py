"""
StudyChart AI - Strict Multi-Tenant User Isolation & Authorization Tests.
Verifies that User A's data is completely invisible and immutable to User B.
"""

import pytest

@pytest.fixture
def user_a_token(client):
    reg_data = {
        "name": "User Alpha",
        "email": "alpha@studychart.ai",
        "password": "PasswordAlpha123!",
        "confirm_password": "PasswordAlpha123!"
    }
    client.post("/api/v1/auth/register", json=reg_data)
    login_resp = client.post("/api/v1/auth/login", json={"email": "alpha@studychart.ai", "password": "PasswordAlpha123!"})
    return login_resp.json()["access_token"]

@pytest.fixture
def user_b_token(client):
    reg_data = {
        "name": "User Beta",
        "email": "beta@studychart.ai",
        "password": "PasswordBeta123!",
        "confirm_password": "PasswordBeta123!"
    }
    client.post("/api/v1/auth/register", json=reg_data)
    login_resp = client.post("/api/v1/auth/login", json={"email": "beta@studychart.ai", "password": "PasswordBeta123!"})
    return login_resp.json()["access_token"]

def test_subject_isolation(client, user_a_token, user_b_token):
    headers_a = {"Authorization": f"Bearer {user_a_token}"}
    headers_b = {"Authorization": f"Bearer {user_b_token}"}

    # User A creates a subject
    create_resp = client.post("/api/v1/subjects", json={
        "name": "Advanced Operating Systems",
        "description": "Kernel design & synchronization",
        "color": "#10b981",
        "icon": "cpu",
        "priority": 5
    }, headers=headers_a)
    assert create_resp.status_code == 201
    subj_a_id = create_resp.json()["id"]

    # User B lists subjects -> should NOT see User A's subject
    list_b_resp = client.get("/api/v1/subjects", headers=headers_b)
    assert list_b_resp.status_code == 200
    b_subjects = list_b_resp.json()
    assert not any(s["id"] == subj_a_id for s in b_subjects)

    # User B attempts to access User A's subject by ID -> Must receive 404 (Resource Not Found)
    get_b_resp = client.get(f"/api/v1/subjects/{subj_a_id}", headers=headers_b)
    assert get_b_resp.status_code == 404

    # User B attempts to delete User A's subject -> Must receive 404
    del_b_resp = client.delete(f"/api/v1/subjects/{subj_a_id}", headers=headers_b)
    assert del_b_resp.status_code == 404

def test_notes_isolation(client, user_a_token, user_b_token):
    headers_a = {"Authorization": f"Bearer {user_a_token}"}
    headers_b = {"Authorization": f"Bearer {user_b_token}"}

    # User A creates a confidential note
    note_resp = client.post("/api/v1/notes", json={
        "title": "Alpha Private Research",
        "content": "Secret algorithms and proprietary heuristics.",
        "tags": "research,private"
    }, headers=headers_a)
    assert note_resp.status_code == 201
    note_a_id = note_resp.json()["id"]

    # User B lists notes -> Note A must not exist in list
    b_notes_resp = client.get("/api/v1/notes", headers=headers_b)
    assert b_notes_resp.status_code == 200
    assert not any(n["id"] == note_a_id for n in b_notes_resp.json())

    # User B attempts to get Note A -> Must return 404
    b_get_resp = client.get(f"/api/v1/notes/{note_a_id}", headers=headers_b)
    assert b_get_resp.status_code == 404

    # User B attempts to patch Note A -> Must return 404
    b_patch_resp = client.patch(f"/api/v1/notes/{note_a_id}", json={"title": "Hacked Title"}, headers=headers_b)
    assert b_patch_resp.status_code == 404
