
from uuid import UUID

from app.domain.task import Task
from app.domain.ports import TaskRepository

class TaskMemoRepository(TaskRepository):
    def __init__(self) -> None:
        self._data: dict[UUID, Task] = {}
        
    def add(self, task: Task) -> None:
        if task.id in self._data:
            raise KeyError('Task already found in memory.')
        self._data[task.id] = task
        
    def list_all(self) -> list[Task]:
        return list(self._data.values())
    
    def get(self, task_id: UUID) -> Task | None:
        return self._data.get(task_id)
    
    def update(self, task: Task) -> None:
        if task.id not in self._data:
            raise KeyError('Task not found in memory.')
        self._data[task.id] = task
        
    def delete(self, task_id: UUID) -> None:
        self._data.pop(task_id, None) # para evitar KeyError si no existe, ponemos el default None
        
    
    
        
    