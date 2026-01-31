
from __future__ import annotations

from pathlib import Path
from datetime import date
import sqlite3
from sqlite3 import Row
from uuid import UUID

from app.domain.ports import TaskRepository
from app.domain.task import Task, TaskStatus
from app.infrastructure.sqlite_repo.sqlite_init_db import _init_db, DB_PATH

class SqliteConexion:
    def __init__(self, path) -> None:
        self.path = path
        self.conexion: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None
        
    def __enter__(self) -> SqliteConexion:
        self.conexion = sqlite3.connect(self.path)
        self.conexion.row_factory = sqlite3.Row
        self.cursor = self.conexion.cursor()
        return self
    
    def __exit__(self, exc_type, exc, tb) -> None:
        if self.conexion is not None:
            try:
                if exc_type is None:
                    self.conexion.commit()
                else:
                    self.conexion.rollback()
            except Exception:
                self.conexion.rollback()
            finally:
                self.conexion.close()
                self.conexion = None
                self.cursor = None                    

class TaskSQLiteRepository(TaskRepository):
    def __init__(self, path: Path = DB_PATH):
        self.path = path
        _init_db(path=path)
        
    def _row_to_task(self, row: Row) -> Task:
        task = Task(
                title=row['title'],
                status=TaskStatus(row['status']),
                project=row['project'],
                notes=row['notes'],
                start_date=date.fromisoformat(row['start_date']) if row['start_date'] is not None else None,
                due_date= date.fromisoformat(row['due_date']) if row['due_date'] is not None else None,
        )
        object.__setattr__(task, 'id', UUID(row['id']))
        return task
        
    def add(self, task: Task) -> None:
        stmt = '''
        INSERT INTO tasks (id, title, status, project, notes, start_date, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        values = (
            str(task.id),
            task.title, 
            task.status.value,
            task.project,
            task.notes,
            task.start_date.isoformat() if task.start_date is not None else None,
            task.due_date.isoformat() if task.due_date is not None else None,
        )
        with SqliteConexion(self.path) as conn:
            assert conn.cursor is not None
            conn.cursor.execute(stmt, values)
    
    def get(self, task_id: UUID) -> Task | None:
        stmt = '''
        SELECT * FROM tasks
        WHERE (id=?)
        '''
        value = (str(task_id),)
        
        with SqliteConexion(self.path) as conn:
            assert conn.cursor is not None
            row = conn.cursor.execute(stmt, value).fetchone()
            
            if not row:
                return None
            
            return self._row_to_task(row)
            
    def list_all(self) -> list[Task]:
        stmt = '''
        SELECT * FROM tasks
        '''
        with SqliteConexion(self.path) as conn:
            assert conn.cursor is not None
            rows = conn.cursor.execute(stmt).fetchall()
            return [self._row_to_task(row) for row in rows]
            
