from flask import Blueprint
from flask_restful import Api
from .main.views import (
    UserCategory,RestaurantResource,UserSignIn,RestaurantById,
    FoodResource,FoodById,RecipeResource,ReviewResource,
    ReviewCategory,InformationResource,OrderResource,UserOrder,
    OrderRetrieve
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
api.add_resource(RecipeResource,'/restaurant/<int:id>/recipe')
api.add_resource(ReviewResource,'/restaurant/<int:id>/reviews')
api.add_resource(ReviewCategory,'/restaurant/<int:r_id>/reviews/<int:id>')
api.add_resource(InformationResource,'/restaurant/<int:id>/information')
api.add_resource(OrderResource,'/order/restaurant/<int:id>')
api.add_resource(UserOrder,'/order/restaurant/<int:id>/food/<int:f_id>')
api.add_resource(OrderRetrieve,'/order/<int:id>/restaurant/<int:r_id>/food/<int:f_id>')