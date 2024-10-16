from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.api_keys.services import *
import logging

# Logger configuration
logger = logging.getLogger(__name__)

# Create Namespace for API keys
api_keys_ns = Namespace('api_keys', description='API key related operations', tags=['api_keys'])

# Define models for input/output with Flask-RESTX
api_key_model = api_keys_ns.model('APIKey', {
    'api_key': fields.String(description='Generated API key')
})

response_model = api_keys_ns.model('Response', {
    'status': fields.String(description='Status of the response'),
    'message': fields.String(description='Message of the response')
})

api_key_list_model = api_keys_ns.model('APIKeyList', {
    'status': fields.String(description='Status of the response'),
    'api_keys': fields.List(fields.String, description='List of API keys')
})


# Generate API Key Resource
@api_keys_ns.route('/generate')
class GenerateApiKey(Resource):
    @jwt_required()
    @api_keys_ns.response(201, 'API key successfully generated', api_key_model)
    @api_keys_ns.response(500, 'Failed to generate API key')
    def post(self):
        """
        Generate a new API key for the current user
        """
        current_user = get_jwt_identity()
        response = generate_api_key_service()
        return {'api_key': response['api_key']}, 201


# Get User API Keys Resource
@api_keys_ns.route('/all')
class GetUserApiKeys(Resource):
    @jwt_required()
    @api_keys_ns.response(200, 'Successfully retrieved API keys', api_key_list_model)
    @api_keys_ns.response(500, 'Failed to retrieve API keys')
    def get(self):
        """
        Get all API keys associated with the current user
        """
        current_user = get_jwt_identity()
        response = get_user_api_keys_service(current_user.get('user_id'))
        return {'status': 'success', 'api_keys': response['api_keys']}, 200


# Delete API Key Resource
@api_keys_ns.route('/<string:api_key>')
class DeleteApiKey(Resource):
    @jwt_required()
    @api_keys_ns.response(200, 'API key successfully deleted', response_model)
    @api_keys_ns.response(404, 'API key not found')
    @api_keys_ns.response(500, 'Failed to delete API key')
    def delete(self, api_key):
        """
        Delete an API key by its value
        """
        current_user = get_jwt_identity()
        delete_api_key_service(api_key, current_user.get('user_id'))
        return {'status': 'success', 'message': 'API key successfully deleted'}, 200
