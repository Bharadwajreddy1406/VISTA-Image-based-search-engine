# global exceptions types are defined here to use across application

class DatabaseCredentialsNotFound(Exception):
    """Exception raised when database credentials are not found in environment variables."""
    def __init__(self, message="Database credentials not found in environment variables."):
        self.message = message
        super().__init__(self.message)

class DatabaseConnectionError(Exception):
    """Exception raised when there is an error connecting to the database."""
    def __init__(self, message="Error connecting to the database."):
        self.message = message
        super().__init__(self.message)
