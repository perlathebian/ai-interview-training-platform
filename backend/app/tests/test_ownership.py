import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_email() -> str:
    return f"ownership-{uuid.uuid4()}@example.com"


def register_and_login(email: str) -> str:
    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "secret123",
            "specialty": "backend",
            "level": "junior",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "secret123",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    return login_response.json()["access_token"]


def test_user_cannot_delete_another_users_resume():
    user_a_token = register_and_login(unique_email())
    user_b_token = register_and_login(unique_email())

    create_response = client.post(
        "/resumes",
        json={
            "raw_text": (
                "Summary\n"
                "Software engineer experienced in Python, FastAPI, React, "
                "PostgreSQL, Docker, APIs, databases, and AI applications."
            )
        },
        headers={
            "Authorization": f"Bearer {user_a_token}",
        },
    )

    assert create_response.status_code == 201

    resume_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/resumes/{resume_id}",
        headers={
            "Authorization": f"Bearer {user_b_token}",
        },
    )

    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Resume not found"


def test_user_cannot_read_another_users_training_target():
    user_a_token = register_and_login(unique_email())
    user_b_token = register_and_login(unique_email())

    create_response = client.post(
        "/training-targets",
        json={
            "target_type": "specific_job",
            "company": "Datadog",
            "role": "Junior Backend Engineer",
            "job_description": "Backend role requiring Python, APIs, databases, and cloud knowledge.",
            "desired_companies": None,
            "focus_areas": ["backend APIs", "databases", "system design"],
        },
        headers={
            "Authorization": f"Bearer {user_a_token}",
        },
    )

    assert create_response.status_code == 201

    target_id = create_response.json()["id"]

    get_response = client.get(
        f"/training-targets/{target_id}",
        headers={
            "Authorization": f"Bearer {user_b_token}",
        },
    )

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Training target not found"