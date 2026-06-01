
from typing import Dict
from .exceptions import DatabaseCredentialsNotFound

def validate_database_settings(DATABASE_SETTINGS: Dict[str, str]):
    required_keys = ["POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]
    missing_keys = [key for key in required_keys if key not in DATABASE_SETTINGS or not DATABASE_SETTINGS[key]]

    if missing_keys:
        raise DatabaseCredentialsNotFound(f"Missing database credentials: {', '.join(missing_keys)}")