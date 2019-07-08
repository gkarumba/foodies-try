from flask import Blueprint
from flask_restful import Api
from .main.views import UserCategory

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(UserCategory, '/user')