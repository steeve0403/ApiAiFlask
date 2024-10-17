class AppErrorBaseClass(Exception):
    """Base class for all application-specific exceptions."""

    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code or 400  # Default status code
        super().__init__(self.message)


class ValidationError(AppErrorBaseClass):
    """Exception raised for validation errors."""

    def __init__(self, message="Invalid input data"):
        super().__init__(message, status_code=400)


class UnauthorizedError(AppErrorBaseClass):
    """Exception raised for unauthorized access."""

    def __init__(self, message="Unauthorized access"):
        super().__init__(message, status_code=401)


class NotFoundError(AppErrorBaseClass):
    """Exception raised when the requested resource is not found."""

    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class ConflictError(AppErrorBaseClass):
    """Exception raised for conflicts, such as an existing record."""

    def __init__(self, message="Conflict occurred"):
        super().__init__(message, status_code=409)


# Token-related errors
class JWTDecodeError(AppErrorBaseClass):
    """Exception raised when there is an error decoding a JWT token."""

    def __init__(self, message="Failed to decode JWT token"):
        super().__init__(message, status_code=401)


class TokenExpiredError(AppErrorBaseClass):
    """Exception raised when a JWT token has expired."""

    def __init__(self, message="Token has expired"):
        super().__init__(message, status_code=401)


class InvalidTokenError(AppErrorBaseClass):
    """Exception raised when a JWT token is invalid."""

    def __init__(self, message="Invalid token"):
        super().__init__(message, status_code=401)
