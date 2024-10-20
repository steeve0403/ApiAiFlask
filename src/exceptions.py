class AppErrorBaseClass(Exception):
    """Base class for all application-specific exceptions."""
    status_code = 400  # Default status code for application errors

    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code or self.status_code  # Use default status code if not provided
        super().__init__(self.message)


class ValidationError(AppErrorBaseClass):
    """Exception raised for validation errors."""
    status_code = 400

    def __init__(self, message="Invalid input data"):
        super().__init__(message, self.status_code)


class UnauthorizedError(AppErrorBaseClass):
    """Exception raised for unauthorized access."""
    status_code = 401

    def __init__(self, message="Unauthorized access"):
        super().__init__(message, self.status_code)


class NotFoundError(AppErrorBaseClass):
    """Exception raised when the requested resource is not found."""
    status_code = 404

    def __init__(self, message="Resource not found"):
        super().__init__(message, self.status_code)


class ConflictError(AppErrorBaseClass):
    """Exception raised for conflicts, such as an existing record."""
    status_code = 409

    def __init__(self, message="Conflict occurred"):
        super().__init__(message, self.status_code)


# Token-related errors
class JWTDecodeError(AppErrorBaseClass):
    """Exception raised when there is an error decoding a JWT token."""
    status_code = 401

    def __init__(self, message="Failed to decode JWT token"):
        super().__init__(message, self.status_code)


class TokenExpiredError(AppErrorBaseClass):
    """Exception raised when a JWT token has expired."""
    status_code = 401

    def __init__(self, message="Token has expired"):
        super().__init__(message, self.status_code)


class InvalidTokenError(AppErrorBaseClass):
    """Exception raised when a JWT token is invalid."""
    status_code = 401

    def __init__(self, message="Invalid token"):
        super().__init__(message, self.status_code)
