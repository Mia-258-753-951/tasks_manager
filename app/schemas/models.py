from pydantic import BaseModel
from datetime import date
from uuid import UUID
from typing import Any

from app.domain.task import TaskStatus

class TaskIn(BaseModel):
    title: str
    status: TaskStatus = TaskStatus.TODO
    project: str | None = None
    notes: str | None = None
    start_date: date | None = None
    due_date: date | None = None
    
class TaskResume(BaseModel):
    id: UUID
    title: str
    project: str | None
    status: TaskStatus
    
class TaskComplete(BaseModel):
    title: str
    status: TaskStatus = TaskStatus.TODO
    project: str | None 
    notes: str | None
    start_date: date | None
    due_date: date | None
    id: UUID
    
class TaskPatch(BaseModel):
    title: str | None = None
    status: TaskStatus | None = None
    project: str | None = None
    notes: str | None = None
    start_date: date | None = None
    due_date: date | None = None
    