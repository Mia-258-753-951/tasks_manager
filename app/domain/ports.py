
from typing import Protocol
from uuid import UUID

from app.domain.task import Task


class TaskRepository(Protocol):
    
    def add(self, task: Task) -> None: ...
    
    def list_all(self) -> list[Task]: ...
    
    def get(self, task_id: UUID) -> Task | None: ...
    
    def update(self, task: Task) -> None: ...
    
    def delete(self,  task_id: UUID) -> None: ...