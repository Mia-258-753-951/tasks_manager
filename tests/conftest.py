
import pytest

from app.api.main import _repo

@pytest.fixture(scope='function', autouse=True)
def reset_repository():
    _repo._data = {}