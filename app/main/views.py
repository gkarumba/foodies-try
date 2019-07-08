from flask import  request
from flask_restful import Resource
from ..models import User, UserSchema, Restaurant, RestaurantSchema
from .. import db,photos
import markdown2 

users_schema = UserSchema(many=True)
user_schema = UserSchema()


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
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return {'message': 'User already exists'}, 400
        user = User(
            username=json_data['username'],
            email=json_data['email'],
            phonenumber=json_data['phonenumber'],
            password_hash=json_data['password_hash'],
            location=json_data['location'],
            role=json_data['role'],
            )
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user).data
        return { "status": 'success', 'data': result }, 201
    
restaurants_schema = RestaurantSchema(many=True)
restaurant_schema = RestaurantSchema()

class RestaurantResource(Resource):
    def get(self):
        restaurant = Restaurant.query.all()
        restaurants = restaurants_schema.dump(restaurant).data
        if restaurants:
            return {
                'status': 'success',
                'data': restaurants
            }, 200
        return {
            'status': 'Failed',
        }, 400
    
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        restaurant = Restaurant.query.filter_by(name=data['name']).first()
        if restaurant:
            
            return {'message': 'User already exists'}, 400
        user = User(
            username=json_data['username'],
            email=json_data['email'],
            phonenumber=json_data['phonenumber'],
            password_hash=json_data['password_hash'],
            location=json_data['location'],
            role=json_data['role'],
            )
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user).data
        return { "status": 'success', 'data': result }, 201