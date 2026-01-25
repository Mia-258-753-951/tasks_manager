
from uuid import UUID, uuid4
from fastapi.testclient import TestClient

from app.schemas.models import TaskResume
from app.api.main import app

client = TestClient(app)

def test_post_tasks():
    payload = {
        'title': 'Tarea1',
    }
    response = client.post('/tasks', json=payload)
    
    assert response.status_code == 201
    task_resume = TaskResume.model_validate(response.json())
    assert isinstance(task_resume.id, UUID)
    
def test_get_tasks():
    payload = {
        'title': 'Tarea2',
    }
    client.post('/tasks', json=payload)
    
    response = client.get('/tasks')
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    
def test_get_task_ok_get_200_status():
    payload = {
        'title': 'Tarea3',
    }
    create = client.post('/tasks', json=payload)
    
    response = client.get(f"/tasks/{create.json()['id']}")
    
    assert response.status_code == 200
    
def test_get_task_with_wrong_id_get_404_status():
    random_id = uuid4()    
    response = client.get(f'/tasks/{random_id}')
    
    assert response.status_code == 404

    