
from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4
from datetime import date


class TaskStatus(str, Enum):
    TODO = 'todo'
    DOING = 'doing'
    DONE = 'done'

@dataclass(frozen=True, slots=True)
class Task:
    title: str
    status: TaskStatus = TaskStatus.TODO
    project: str | None = None
    notes: str | None = None
    start_date: date | None = None
    due_date: date | None = None
    id: UUID = field(init=False)
    
    def __post_init__(self) -> None:
        title_normalize = (self.title or "").strip()
        if not title_normalize:
            raise ValueError("The 'title' field is requierd.")
        if (self.due_date and self.start_date) and self.start_date > self.due_date:
            raise ValueError("task must start before or at due date.")
        
        object.__setattr__(self, 'title', title_normalize)  # Si usamos frozen, los atributos hay que cambiarlos así.
        object.__setattr__(self, 'id', uuid4())
        
    
    