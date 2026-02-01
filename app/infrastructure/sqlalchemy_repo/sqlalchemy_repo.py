from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select
from uuid import UUID

from app.domain.ports import TaskRepository
from app.domain.task import Task
from app.infrastructure.sqlalchemy_repo.orm_models import TaskRow


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: sessionmaker[Session]):
        self.session_factory = session
        
    def _task_to_row(self, task: Task) -> TaskRow:
        return TaskRow(
            id=task.id,
            title=task.title,
            status=task.status,
            project=task.project,
            notes=task.notes,
            start_date=task.start_date,
            due_date=task.due_date,
        )
        
    def _row_to_task(self, row: TaskRow) -> Task:
        task = Task(
            title=row.title,
            status=row.status,
            project=row.project,
            notes=row.notes,
            start_date=row.start_date,
            due_date=row.due_date,
        )
        object.__setattr__(task, 'id', row.id)
        return task
        
    def add(self, task: Task) -> None:
        with self.session_factory.begin() as s:
            row = s.get(TaskRow, task.id)
            if row:
                raise KeyError(f'Task already exists with id {task.id}')
            row = self._task_to_row(task)
            s.add(row)            

    def get(self, task_id: UUID) -> Task | None:
        with self.session_factory() as s:
            row = s.get(TaskRow, task_id)
            if row is None:
                return None
            return self._row_to_task(row)
    
    def list_all(self) -> list[Task]:
        stmt = select(TaskRow)
        with self.session_factory() as s:
            rows = s.scalars(stmt).all()
            return [self._row_to_task(row) for row in rows]
    
    def update(self, task: Task) -> None:
        with self.session_factory.begin() as s:
            row = s.get(TaskRow, task.id)
            if row is None:
                raise KeyError(f'Task not found with id {task.id}.')
            row.title = task.title
            row.status = task.status
            row.start_date = task.start_date
            row.due_date = task.due_date
            row.notes = task.notes
            row.project = task.project            
    
    def delete(self, task_id: UUID) -> None:
        with self.session_factory.begin() as s:
            row = s.get(TaskRow, task_id)
            if row is None:
                raise KeyError(f'Task not found with id {task_id}.')
            s.delete(row)
            
    
        
        
