class AppErrorBaseClass(Exception):
    """Base class for all application-specific exceptions."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ValidationError(AppErrorBaseClass):
    """Exception levée pour les erreurs de validation."""
    def __init__(self, message="Invalid input data"):
        super().__init__(message)

class UnauthorizedError(AppErrorBaseClass):
    """Exception levée en cas d'accès non autorisé."""
    def __init__(self, message="Unauthorized access"):
        super().__init__(message)

class NotFoundError(AppErrorBaseClass):
    """Exception levée lorsque la ressource demandée est introuvable."""
    def __init__(self, message="Resource not found"):
        super().__init__(message)

class ConflictError(AppErrorBaseClass):
    """Exception levée pour les conflits, comme l'enregistrement existant."""
    def __init__(self, message="Conflict occurred"):
        super().__init__(message)
