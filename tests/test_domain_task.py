import pytest
from datetime import date

from app.domain.task import Task, TaskStatus

def test_create_task_assign_id():
    task = Task(title='Nueva tarea para test')    
    assert task.id is not None
    
def test_create_task_raises_with_empty_title():    
    with pytest.raises(ValueError):
        Task(title='    ')
        
def test_create_task_raises_if_due_before_start():
    with pytest.raises(ValueError):
        Task(title='Prueba', start_date=date(2025, 1, 15), due_date=date(2025, 1, 10))
        
def test_title_get_normalized():
    task = Task(title=' Hola ')    
    assert task.title == 'Hola'

def test_default_status_is_todo():
    task = Task(title='Nueva tarea para test')
    assert task.status == TaskStatus.TODO