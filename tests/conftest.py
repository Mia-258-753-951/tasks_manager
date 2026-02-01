
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.api.main import app, get_repository
from app.infrastructure.sqlalchemy_repo.orm_models import Base
from app.infrastructure.sqlalchemy_repo.sqlalchemy_repo import SqlAlchemyTaskRepository

@pytest.fixture(scope='function')
def get_session(tmp_path):
    db_path = tmp_path / 'test_db.db'
    engine = create_engine(
        f'sqlite:///{db_path}', 
        connect_args={'check_same_thread': False}, 
        echo=False, 
        future=True
        )
    # creamos el esquema en db_test.db
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    #pasamos el sessionmaker que usará nuestro repositorio en test
    yield SessionLocal
    
@pytest.fixture(scope='function', autouse=True)
def override_repository(get_session):
    # definimos la función que reemplazará a la original
    def get_repository_override():
        return SqlAlchemyTaskRepository(get_session)
    #aplicamos el override
    app.dependency_overrides[get_repository] = get_repository_override
    
    yield
    
    # limpiamos al acabar el test
    app.dependency_overrides.clear()
    
    
