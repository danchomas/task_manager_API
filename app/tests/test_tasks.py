# tests/test_tasks.py
import pytest
from uuid import UUID, uuid4

def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={"name": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "created"
    assert UUID(data["id"])

def test_get_task(client):
    create_response = client.post(
        "/tasks/",
        json={"name": "Test Task"}
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["name"] == "Test Task"

def test_get_nonexistent_task(client):
    response = client.get(f"/tasks/{uuid4()}")
    assert response.status_code == 404

def test_get_tasks(client):
    for i in range(3):
        client.post("/tasks/", json={"name": f"Task {i}"})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_update_task(client):
    create_response = client.post("/tasks/", json={"name": "Original Task"})
    task_id = create_response.json()["id"]

    update_response = client.put(
        f"/tasks/{task_id}",
        json={"name": "Updated Task", "status": "in_progress"}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Updated Task"
    assert data["status"] == "in_progress"

def test_update_nonexistent_task(client):
    response = client.put(
        f"/tasks/{uuid4()}",
        json={"name": "Updated Task"}
    )
    assert response.status_code == 404

def test_delete_task(client):
    create_response = client.post("/tasks/", json={"name": "To be deleted"})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_task(client):
    response = client.delete(f"/tasks/{uuid4()}")
    assert response.status_code == 404

def test_invalid_status(client):
    response = client.post(
        "/tasks/",
        json={"name": "Test", "status": "invalid_status"}
    )
    assert response.status_code == 422
