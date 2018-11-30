
from enum import Enum

class db_type(Enum):
    """Enum method to make the database selection more readable"""
    POSTGRES_DB = 1
    SQLITE_DB = 2
