from flask import Blueprint
from flask_restful import Api
from .main.views import (
    UserCategory,RestaurantResource,UserSignIn,RestaurantById,
    FoodResource,FoodById,RecipeResource,ReviewResource,
    ReviewCategory,InformationResource,OrderResource,UserOrder,
    OrderRetrieve,RestaurantCategory,RestaurantLocation
)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
# user registration
api.add_resource(UserCategory, '/user/registration')
# get all/ add restaurant 
api.add_resource(RestaurantResource, '/restaurant')
# search restaurant by name
api.add_resource(RestaurantCategory,'/restaurant/<uname>')
# user login
api.add_resource(UserSignIn,'/user/login')
# search restaurant by location
api.add_resource(RestaurantCategory,'/restaurant/location/<uname>')
# get/edit/delete restaurant by id (id=restaurant_id)
api.add_resource(RestaurantById,'/restaurant/<int:id>')
# get/add food to specific restaurant(id=restaurant_id)
api.add_resource(FoodResource,'/restaurant/<int:id>/foods')
# get/edit/delete food by id from specific restaurant (r_id= restaurant_id,f_id=food_id)
api.add_resource(FoodById,'/restaurant/<int:r_id>/foods/<int:f_id>')
# get/add/edit/delete recipe from specific restaurant (id=restaurant_id)
api.add_resource(RecipeResource,'/restaurant/<int:id>/recipe')
# get/add review to specific restaurant (id=restaurant_id)
api.add_resource(ReviewResource,'/restaurant/<int:id>/reviews')
# edit/delete review of specific restaurant (r_id=restaurant_id, id=review_id)
api.add_resource(ReviewCategory,'/restaurant/<int:r_id>/reviews/<int:id>')
# get/add/edit/delete recipe from specific restaurant (id=restaurant_id)
api.add_resource(InformationResource,'/restaurant/<int:id>/information')
# get order by restaurant (id=restaurant_id)
api.add_resource(OrderResource,'/order/restaurant/<int:id>')
# post order by restaurant and food id (r_id= restaurant_id,f_id=food_id)
api.add_resource(UserOrder,'/order/restaurant/<int:id>/food/<int:f_id>')
# edi/delete order (id=order_id,r_id= restaurant_id,f_id=food_id)
api.add_resource(OrderRetrieve,'/order/<int:id>/restaurant/<int:r_id>/food/<int:f_id>')