
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.sqlalchemy_repo.orm_models import Base

DB_PATH = Path(__file__).parents[2] / 'data'/ 'tasks_data.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(
    f'sqlite:///{DB_PATH}', 
    connect_args={'check_same_thread':False},  # SQLite + FastAPI
    echo=False, future=True
    )    
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db():
    Base.metadata.create_all(bind=engine)
    
