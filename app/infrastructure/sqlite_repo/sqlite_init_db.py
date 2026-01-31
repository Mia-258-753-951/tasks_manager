
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parents[2] / 'data' / 'sqlite.db'

create_table = '''
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    project TEXT,
    notes TEXT,
    start_date TEXT,
    due_date TEXT
    );
    '''

def _init_db(path: Path=DB_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(path)
    cursor = conexion.cursor()
    cursor.execute(create_table)
    conexion.commit()
    conexion.close()
    
    
    
    
if __name__ == '__main__':
    _init_db()
    