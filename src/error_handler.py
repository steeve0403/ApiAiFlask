import logging
from flask import jsonify
from src.exceptions import ValidationError, UnauthorizedError, NotFoundError, AppErrorBaseClass, ConflictError

# Configurer le logger
logger = logging.getLogger(__name__)

def handle_validation_error(error):
    logger.error(f"Validation Error: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), 400

def handle_unauthorized_error(error):
    logger.error(f"Unauthorized Access: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), 401

def handle_not_found_error(error):
    logger.error(f"Resource Not Found: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), 404

def handle_conflict_error(error):
    logger.error(f"Conflict Error: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), 409

def handle_app_error(error):
    logger.error(f"Application Error: {str(error)}")
    return jsonify({'status': 'failed', 'message': error.message}), 400

def handle_generic_exception(error):
    logger.error(f"Unexpected Error: {str(error)}")
    return jsonify({'status': 'failed', 'message': 'An unexpected error occurred', 'error': str(error)}), 500
