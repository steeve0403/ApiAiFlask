import logging
from flask import jsonify
from src.exceptions import ValidationError, UnauthorizedError, NotFoundError, AppErrorBaseClass, ConflictError, \
    JWTDecodeError, TokenExpiredError, InvalidTokenError

logger = logging.getLogger(__name__)


def handle_validation_error(error):
    logger.error(f"Validation Error: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), error.status_code


def handle_unauthorized_error(error):
    logger.error(f"Unauthorized Access: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), error.status_code


def handle_not_found_error(error):
    logger.error(f"Resource Not Found: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), error.status_code


def handle_conflict_error(error):
    logger.error(f"Conflict Error: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), error.status_code


def handle_jwt_decode_error(error):
    logger.error(f"JWT Decode Error: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), error.status_code


def handle_token_expired_error(error):
    logger.warning(f"Token Expired: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), error.status_code


def handle_invalid_token_error(error):
    logger.warning(f"Invalid Token: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), error.status_code


def handle_app_error(error):
    logger.error(f"Application Error: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), error.status_code


def handle_generic_exception(error):
    logger.error(f"Unexpected Error: {str(error)}")
    return jsonify({'status': 'failed', 'message': 'An unexpected error occurred', 'error': str(error)}), 500


def register_error_handlers(app):
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(UnauthorizedError, handle_unauthorized_error)
    app.register_error_handler(NotFoundError, handle_not_found_error)
    app.register_error_handler(ConflictError, handle_conflict_error)
    app.register_error_handler(JWTDecodeError, handle_jwt_decode_error)
    app.register_error_handler(TokenExpiredError, handle_token_expired_error)
    app.register_error_handler(InvalidTokenError, handle_invalid_token_error)
    app.register_error_handler(AppErrorBaseClass, handle_app_error)
    app.register_error_handler(Exception, handle_generic_exception)
