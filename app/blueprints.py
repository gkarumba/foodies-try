from flask import Blueprint
from flask_restful import Api
from .main.views import (
    UserCategory,RestaurantResource,UserSignIn,RestaurantById,
    FoodResource,FoodById
)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(UserCategory, '/user')
api.add_resource(RestaurantResource, '/restaurant')
api.add_resource(UserSignIn,'/login')
api.add_resource(RestaurantById,'/restaurant/<int:id>')
api.add_resource(FoodResource,'/restaurant/<int:id>/foods')
api.add_resource(FoodById,'/restaurant/<int:r_id>/foods/<int:f_id>')