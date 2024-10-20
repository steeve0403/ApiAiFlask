import logging
from flask import jsonify, render_template
from src.exceptions import (
    ValidationError, UnauthorizedError, NotFoundError, ConflictError,
    JWTDecodeError, TokenExpiredError, InvalidTokenError, AppErrorBaseClass
)

logger = logging.getLogger(__name__)


# Standard JSON response structure for all errors
def generate_json_response(error):
    return jsonify({'status': 'failed', 'message': error.message}), error.status_code


# Generic error handler for non-handled exceptions (500 or unexpected)
def handle_generic_exception(error):
    logger.error(f"Unexpected Error: {str(error)}")
    return jsonify({'status': 'failed', 'message': 'An unexpected error occurred'}), 500


# Specific handlers for each custom error type
def handle_validation_error(error):
    logger.error(f"Validation Error: {str(error)}")
    return generate_json_response(error)


def handle_unauthorized_error(error):
    logger.error(f"Unauthorized Error: {str(error)}")
    return render_template('401.html'), 401  # Render HTML for 401


def handle_forbidden_error(error):
    logger.error(f"Forbidden Error: {str(error)}")
    return render_template('403.html'), 403  # Render HTML for 403


def handle_not_found_error(error):
    logger.error(f"404 Error: {str(error)}")
    return render_template('404.html'), 404  # Render HTML for 404


def handle_method_not_allowed_error(error):
    logger.error(f"Method Not Allowed Error: {str(error)}")
    return render_template('405.html'), 405  # Render HTML for 405


def handle_internal_server_error(error):
    logger.error(f"Internal Server Error: {str(error)}")
    return render_template('500.html'), 500  # Render HTML for 500


def handle_conflict_error(error):
    logger.error(f"Conflict Error: {str(error)}")
    return generate_json_response(error)


def handle_jwt_decode_error(error):
    logger.error(f"JWT Decode Error: {str(error)}")
    return generate_json_response(error)


def handle_token_expired_error(error):
    logger.warning(f"Token Expired: {str(error)}")
    return generate_json_response(error)


def handle_invalid_token_error(error):
    logger.warning(f"Invalid Token: {str(error)}")
    return generate_json_response(error)


# Function to register all error handlers in the Flask app
def register_error_handlers(app):
    app.register_error_handler(401, handle_unauthorized_error)
    app.register_error_handler(403, handle_forbidden_error)
    app.register_error_handler(404, handle_not_found_error)
    app.register_error_handler(405, handle_method_not_allowed_error)
    app.register_error_handler(500, handle_internal_server_error)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(UnauthorizedError, handle_unauthorized_error)
    app.register_error_handler(NotFoundError, handle_not_found_error)  # HTML page for 404
    app.register_error_handler(ConflictError, handle_conflict_error)
    app.register_error_handler(JWTDecodeError, handle_jwt_decode_error)
    app.register_error_handler(TokenExpiredError, handle_token_expired_error)
    app.register_error_handler(InvalidTokenError, handle_invalid_token_error)
    app.register_error_handler(AppErrorBaseClass, handle_generic_exception)  # Catch-all for app errors
    app.register_error_handler(Exception, handle_generic_exception)  # Catch-all for unexpected exceptions
