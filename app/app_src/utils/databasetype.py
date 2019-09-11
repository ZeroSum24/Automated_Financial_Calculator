
from enum import Enum


class DatabaseType(Enum):
    """
    Enum class to make the database selection more readable
    """
    POSTGRES_DB = 1
    SQLITE_DB = 2
