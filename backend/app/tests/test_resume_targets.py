import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_email() -> str:
    return f"context-{uuid.uuid4()}@example.com"


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

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "secret123",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    return response.json()["access_token"]


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_create_resume():
    token = register_and_login(unique_email())

    response = client.post(
        "/resumes",
        json={
            "raw_text": (
                "Summary\n"
                "Backend engineer experienced in Python, FastAPI, PostgreSQL, "
                "Docker, React, APIs, databases, and machine learning projects.\n\n"
                "Projects\n"
                "AI Interview Platform using FastAPI and React\n\n"
                "Education\n"
                "BSc Computer Science"
            )
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["is_active"] is True
    assert data["is_deleted"] is False
    assert "python" in data["extracted_skills"]
    assert "fastapi" in data["extracted_skills"]


def test_fetch_own_resume():
    token = register_and_login(unique_email())

    client.post(
        "/resumes",
        json={
            "raw_text": (
                "Summary\n"
                "Frontend engineer experienced in React, TypeScript, JavaScript, "
                "Tailwind, Docker, Git, and modern web applications.\n\n"
                "Projects\n"
                "Design system and dashboard platform\n\n"
                "Education\n"
                "BSc Computer Science"
            )
        },
        headers=auth_headers(token),
    )

    response = client.get(
        "/resumes/me",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["is_active"] is True
    assert "react" in data["extracted_skills"]


def test_user_cannot_delete_another_users_resume():
    user_a_token = register_and_login(unique_email())
    user_b_token = register_and_login(unique_email())

    create_response = client.post(
        "/resumes",
        json={
            "raw_text": (
                "Summary\n"
                "Senior frontend engineer experienced in React, TypeScript, "
                "Next.js, Docker, AWS, component libraries, and frontend architecture."
            )
        },
        headers=auth_headers(user_a_token),
    )

    assert create_response.status_code == 201

    resume_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/resumes/{resume_id}",
        headers=auth_headers(user_b_token),
    )

    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Resume not found"


def test_create_training_target():
    token = register_and_login(unique_email())

    response = client.post(
        "/training-targets",
        json={
            "target_type": "specific_job",
            "company": "Datadog",
            "role": "Junior Backend Engineer",
            "job_description": "Backend role requiring Python, APIs, databases, cloud, and system design.",
            "desired_companies": None,
            "focus_areas": ["backend APIs", "databases", "system design"],
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "Datadog"
    assert data["role"] == "Junior Backend Engineer"
    assert "databases" in data["focus_areas"]


def test_fetch_training_target():
    token = register_and_login(unique_email())

    create_response = client.post(
        "/training-targets",
        json={
            "target_type": "specific_job",
            "company": "OpenAI",
            "role": "Backend Engineer",
            "job_description": "Backend engineering role focused on APIs, infrastructure, reliability, and AI systems.",
            "desired_companies": None,
            "focus_areas": ["APIs", "infrastructure", "reliability"],
        },
        headers=auth_headers(token),
    )

    target_id = create_response.json()["id"]

    response = client.get(
        f"/training-targets/{target_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == target_id
    assert data["company"] == "OpenAI"
    assert data["role"] == "Backend Engineer"


def test_user_cannot_fetch_another_users_training_target():
    user_a_token = register_and_login(unique_email())
    user_b_token = register_and_login(unique_email())

    create_response = client.post(
        "/training-targets",
        json={
            "target_type": "specific_job",
            "company": "Stripe",
            "role": "Backend Engineer",
            "job_description": "Backend role involving APIs, payments, databases, and distributed systems.",
            "desired_companies": None,
            "focus_areas": ["payments", "databases", "distributed systems"],
        },
        headers=auth_headers(user_a_token),
    )

    target_id = create_response.json()["id"]

    response = client.get(
        f"/training-targets/{target_id}",
        headers=auth_headers(user_b_token),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Training target not found"