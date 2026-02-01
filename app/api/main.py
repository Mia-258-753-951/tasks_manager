
from fastapi import FastAPI, Depends, HTTPException
from uuid import UUID
from contextlib import asynccontextmanager
from dataclasses import replace, asdict

from app.domain.ports import TaskRepository
from app.domain.task import Task
from app.infrastructure.sqlalchemy_repo.sqlalchemy_repo import SqlAlchemyTaskRepository
from app.schemas.models import TaskIn, TaskResume, TaskComplete, TaskPatch
from app.infrastructure.sqlalchemy_repo.db import SessionLocal, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title='Task Manager', lifespan=lifespan)

_repo = SqlAlchemyTaskRepository(SessionLocal)

def get_repository() -> TaskRepository:
    return _repo

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/tasks', response_model=TaskResume, status_code=201)
def add_task(
    payload: TaskIn, 
    repository: TaskRepository = Depends(get_repository)
    ):
    new_task = Task(
        title=payload.title,
        status=payload.status,
        project=payload.project,
        notes=payload.notes,
        start_date=payload.start_date,
        due_date=payload.due_date,
    )
    repository.add(new_task)
    return TaskResume(
        id=new_task.id,
        title=new_task.title,
        project=new_task.project,
        status=new_task.status,
    )

@app.get('/tasks', response_model=list[TaskResume])
def read_all_tasks(repository: TaskRepository = Depends(get_repository)):
    tasks = repository.list_all()
    return [
        TaskResume(id=t.id, title=t.title, project=t.project, status=t.status)
        for t in tasks
        ]

@app.get('/tasks/{task_id}', response_model=TaskComplete)
def read_task(
    task_id: UUID,
    repository: TaskRepository = Depends(get_repository)
    ):
    task = repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=('task not found.'))
    return TaskComplete(
        id=task.id,
        title=task.title,
        status=task.status,
        project=task.project,
        notes=task.notes,
        start_date=task.start_date,
        due_date=task.due_date,
    )
    
@app.delete('/tasks/{task_id}', status_code=204)
def delete_task(
    task_id: UUID, 
    repository: TaskRepository = Depends(get_repository)
    ):
    
    task = repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='task not found.')
    repository.delete(task_id)
    
# helper para update 
def _with_updates(task: Task, **changes) -> Task:
    updated = replace(task, **changes)
    object.__setattr__(updated, "id", task.id)
    return updated

@app.patch('/tasks/{task_id}', response_model=TaskComplete)
def patch_task(
    task_id: UUID,
    payload: TaskPatch,
    repository: TaskRepository = Depends(get_repository),
    ):
    
    task = repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='task not found.')   
    
    # obtenemos diccinario con los valores aportados por cliente, excluyendo los no aportados    
    changes = payload.model_dump(exclude_unset=True)
    
    # creamos una instancia nueva actualizada con replace de dataclasess      
    updated_task = _with_updates(task, **changes)
        
    repository.update(updated_task)
    
    return asdict(updated_task)
        
    
        
        
        
    

    
    
    
    
        
