from flask import  request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_restful import Resource
from ..models import(
    User, UserSchema, Restaurant, RestaurantSchema, LoginSchema,
    Food,FoodSchema,Recipe,RecipeSchema) 
from .. import db,photos
import markdown2 
from ..util.tokens import Tokens,login_required

tk = Tokens() 

users_schema = UserSchema(many=True)
user_schema = UserSchema()
login_schema = LoginSchema()     
restaurants_schema = RestaurantSchema(many=True)
restaurant_schema = RestaurantSchema()
foods_schema = FoodSchema(many=True)
food_schema = FoodSchema()

# @main.route('/users', methods=['POST'])
class UserCategory(Resource):
    '''
    View root page function that returns the index page and its data
    '''
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users).data
        return {
            'status': 'success',
            'data': users
        }, 200
    
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {'message': 'User with email provided already exists'}, 400
        user = User(
            username=json_data['username'],
            email=json_data['email'],
            phonenumber=json_data['phonenumber'],
            password_hash=generate_password_hash(json_data['password_hash']),
            location=json_data['location'],
            role=json_data['role'],
            )
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user).data
        return { "status": 'success', 'data': result }, 201
 
class UserSignIn(Resource):
    def post(self):
        """Method to allow user to login"""
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = login_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {'message': 'No User exists with that email'}, 400
        if user:
            if user.verify_password(data['password_hash']):
                user_id = user.id
                user_token = tk.generate_token(user_id)
                if not user_token:
                    return {
                    'message':'Token Generation Unsuccessful'
                },401
                return {
                        'message':'User logged in successfully',
                        'user_id': user_id,
                        'token': user_token
                    },200
            return {
                'message':'Invalid logging credentials'
            },400

class RestaurantResource(Resource):
    @login_required
    def get(self):
        restaurant = Restaurant.query.all()
        restaurants = restaurants_schema.dump(restaurant).data
        if restaurants:
            return {
                'status': 'success',
                'data': restaurants
            }, 200
        return {
            'status': 'No restaurants found',
        }, 400
    
    @login_required
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = restaurant_schema.load(json_data)
        if errors:
            return errors, 422
        restaurant = Restaurant.query.filter_by(name=data['name']).first()
        print(restaurant)
        if restaurant:
            if restaurant.location == data['location']:            
                return {'message': 'Restaurant already exists in that location'}, 400
        restaurant = Restaurant(
            name=json_data['name'],
            location=json_data['location'],
            )
        db.session.add(restaurant)
        db.session.commit()
        result = restaurant_schema.dump(restaurant).data
        return { "status": 'success', 'data': result }, 201
    
class RestaurantById(Resource):
    @login_required
    def get(self,id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        print(restaurant)
        restaurants = restaurant_schema.dump(restaurant).data
        if restaurants:
            return {
                'status': 'success',
                'data': restaurants
            }, 200
        return {
            'status': 'No restaurant found',
        }, 400
        
    @login_required
    def put(self,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = restaurant_schema.load(json_data)
        if errors:
            return errors, 422
        restaurant = Restaurant.query.filter_by(id=id).first()
        # print(restaurant)
        if not restaurant:
            return {'message': 'restaurant does not exist'}, 400
        restaurant.name = data['name']
        restaurant.location=data['location']
        db.session.commit()
        # restaurants = Restaurant.query.filter_by(id=id).first()
        result = restaurant_schema.dump(restaurant).data
        print(result)
        if result:
            return {
                "status" : 'success',
                'data' : result,
            }, 200
        
    @login_required
    def delete(self,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = restaurant_schema.load(json_data)
        if errors:
            return errors, 422
        restaurants = Restaurant.query.filter_by(id=id).first()
        # print(restaurant)
        if not restaurants:
            return {'message': 'restaurant does not exist'}, 400
        restaurant = Restaurant.query.filter_by(id=id).delete()
        db.session.commit()

        result = restaurant_schema.dump(restaurant).data

        return { "status": 'success', 'data': result}, 204

class FoodResource(Resource):
    @login_required
    def get(self,id):
        food = Food.query.filter_by(restaurant_id=id).all()
        foods = foods_schema.dump(food).data
        if foods:
            return {
                'status': 'success',
                'data': foods
            }, 200
        return {
            'status': 'No foods found',
        }, 400
    
    @login_required
    def post(self,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = food_schema.load(json_data)
        if errors:
            return errors, 422
        food = Food.query.filter_by(foods=data['foods'],restaurant_id=id).first()
        # print(food)
        if food:           
            return {'message': 'food already exists in that restaurant'}, 400
        food = Food(
            foods=json_data['foods'],
            category=json_data['category'],
            description=json_data['description'],
            price=json_data['price'],
            restaurant_id=id
            )
        print(food.restaurant_id)
        food.restaurant_id = id
        db.session.add(food)
        db.session.commit()
        result = food_schema.dump(food).data
        return { "status": 'success', 'data': result }, 201
    
class FoodById(Resource):
    @login_required
    def get(self,r_id,f_id):
        food = Food.query.filter_by(id=f_id,restaurant_id=r_id).first()
        print(food)
        foods = food_schema.dump(food).data
        if foods:
            return {
                'status': 'success',
                'data': foods
            }, 200
        return {
            'status': 'No food found',
        }, 400
        
    @login_required
    def put(self,r_id,f_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = food_schema.load(json_data)
        if errors:
            return errors, 422
        food = Food.query.filter_by(id=f_id,restaurant_id=r_id).first()
        # print(restaurant)
        if not food:           
            return {'message': 'food does not exists'}, 400
        food.foods = data['foods']
        food.category=data['category']
        food.description=data['description']
        food.price=data['price']
        food.restaurant_id=data['restaurant_id']
        food.restaurant_id= r_id
        db.session.commit()
        # restaurants = Restaurant.query.filter_by(id=id).first()
        result = food_schema.dump(food).data
        print(result)
        if result:
            return {
                "status" : 'success',
                'data' : result,
            }, 200
        
    @login_required
    def delete(self,r_id,f_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = food_schema.load(json_data)
        if errors:
            return errors, 422
        food = Food.query.filter_by(id=f_id,restaurant_id=r_id).first()
        # print(restaurant)
        if not food:           
            return {'message': 'food does not exists'}, 400
        food = Food.query.filter_by(id=f_id,restaurant_id=r_id).delete()
        db.session.commit()

        result = food_schema.dump(food).data

        return { "status": 'success', 'data': result}, 204
    
class RecipeResource(Resource):
    @login_required
    def get(self,id):
        food = Food.query.filter_by(restaurant_id=id).all()
        foods = foods_schema.dump(food).data
        if foods:
            return {
                'status': 'success',
                'data': foods
            }, 200
        return {
            'status': 'No foods found',
        }, 400
    
    @login_required
    def post(self,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = food_schema.load(json_data)
        if errors:
            return errors, 422
        food = Food.query.filter_by(foods=data['foods'],restaurant_id=id).first()
        # print(food)
        if food:           
            return {'message': 'food already exists in that restaurant'}, 400
        food = Food(
            foods=json_data['foods'],
            category=json_data['category'],
            description=json_data['description'],
            price=json_data['price'],
            restaurant_id=id
            )
        print(food.restaurant_id)
        food.restaurant_id = id
        db.session.add(food)
        db.session.commit()
        result = food_schema.dump(food).data
        return { "status": 'success', 'data': result }, 201
    