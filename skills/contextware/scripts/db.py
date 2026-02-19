import lancedb
import os
from lancedb.pydantic import LanceModel, Vector
from pydantic import Field
from typing import List, Optional
import time

# Use an absolute path for the DB to avoid issues with different working directories
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "data", "contextware_db")

class Fact(LanceModel):
    content: str
    vector: Vector(384)

class Episode(LanceModel):
    goal: str
    summary: str
    result: str  # success | failure | partial
    category: str
    timestamp: float = Field(default_factory=time.time)
    vector: Vector(384)

class CodeIndex(LanceModel):
    file_path: str
    summary: str
    classes: List[str]
    functions: List[str]
    last_modified: float
    vector: Vector(384)

_db_connection = None

def get_db():
    global _db_connection
    if _db_connection is None:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        _db_connection = lancedb.connect(DB_PATH)
    return _db_connection

def get_table(name: str, schema=None):
    db = get_db()
    if name in db.table_names():
        return db.open_table(name)
    if schema is None:
        if name == "facts": schema = Fact
        elif name == "episodes": schema = Episode
        elif name == "code_index": schema = CodeIndex
        else: raise ValueError(f"Unknown table and no schema provided: {name}")
    return db.create_table(name, schema=schema)
