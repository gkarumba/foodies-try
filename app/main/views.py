from flask import  request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_restful import Resource
from ..models import(
    User, UserSchema, Restaurant, RestaurantSchema, LoginSchema,
    Food,FoodSchema,Recipe,RecipeSchema, Review, ReviewSchema,
    Information,InformationSchema,Order,OrderSchema) 
from .. import db,photos
import markdown2 
from datetime import datetime
from ..util.tokens import Tokens,login_required, GetUserId

tk = Tokens() 

users_schema = UserSchema(many=True)
user_schema = UserSchema()
login_schema = LoginSchema()     
restaurants_schema = RestaurantSchema(many=True)
restaurant_schema = RestaurantSchema()
foods_schema = FoodSchema(many=True)
food_schema = FoodSchema()
recipes_schema = RecipeSchema(many=True)
recipe_schema = RecipeSchema()
reviews_schema = ReviewSchema(many=True)
review_schema = ReviewSchema()
informations_schema = InformationSchema(many=True)
information_schema = InformationSchema()
orders_schema = OrderSchema(many=True)
order_schema = OrderSchema()

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
class RestaurantCategory(Resource):
    @login_required
    def get(self,uname):
        restaurant = Restaurant.query.filter_by(name=uname).first()
        restaurants = restaurants_schema.dump(restaurant).data
        if restaurants:
            return {
                'status': 'success',
                'data': restaurants
            }, 200
        return {
            'status': 'No restaurants found',
        }, 400
        
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
            image_url = json_data['image_url']
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
        restaurant.image_url=data['image_url']
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
        recipe = Recipe.query.filter_by(restaurant_id=id).all()
        recipes = recipes_schema.dump(recipe).data
        if recipes:
            return {
                'status': 'success',
                'data': recipes
            }, 200
        return {
            'status': 'No recipes found',
        }, 400
    
    @login_required
    def post(self,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = recipe_schema.load(json_data)
        if errors:
            return errors, 422
        recipe = Recipe.query.filter_by(recipe_name=data['recipe_name'],restaurant_id=id).first()
        # print(recipe)
        if recipe:           
            return {'message': 'recipe already exists in that restaurant'}, 400
        recipe = Recipe(
            recipe_name=json_data['recipe_name'],
            description=json_data['description'],
            restaurant_id=id
            )
        print(recipe.restaurant_id)
        recipe.restaurant_id = id
        db.session.add(recipe)
        db.session.commit()
        result = recipe_schema.dump(recipe).data
        return { "status": 'success', 'data': result }, 201
           
    @login_required
    def put(self,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = recipe_schema.load(json_data)
        if errors:
            return errors, 422
        recipe = Recipe.query.filter_by(restaurant_id=id).first()
        # print(recipe)
        if not recipe:           
            return {'message': 'recipe does not exists in that restaurant'}, 400
        
        recipe.recipe_name=data['recipe_name']
        recipe.description=data['description']
        recipe.restaurant_id=data['restaurant_id']
        recipe.restaurant_id= id
        db.session.commit()
        # restaurants = Restaurant.query.filter_by(id=id).first()
        result = recipe_schema.dump(recipe).data
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
        data, errors = recipe_schema.load(json_data)
        if errors:
            return errors, 422
        recipe = Recipe.query.filter_by(restaurant_id=id).first()
        # print(recipe)
        if not recipe:           
            return {'message': 'recipe does not exists in that restaurant'}, 400
        recipe = Recipe.query.filter_by(restaurant_id=id).delete()
        db.session.commit()

        result = recipe_schema.dump(recipe).data

        return { "status": 'success', 'data': result}, 204
    
class ReviewResource(Resource):
    @login_required
    def get(self,id):
        review = Review.query.filter_by(restaurant_id=id).all()
        reviews = reviews_schema.dump(review).data
        if reviews:
            return {
                'status': 'success',
                'data': reviews
            }, 200
        return {
            'status': 'No reviews found',
        }, 400
    
    @login_required
    def post(self,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = review_schema.load(json_data)
        if errors:
            return errors, 422
        # review = Review.query.filter_by(review_name=data['review_name'],restaurant_id=id).first()
        # # print(review)
        # if review:           
        #     return {'message': 'review already exists in that restaurant'}, 400
        userId = GetUserId.user_creds(self)
        print(userId)
        review = Review(
            review=json_data['review'],
            rating=json_data['rating'],
            # posted = json_data['posted'],
            user_id = userId,
            restaurant_id=id
            )
        print(review.restaurant_id)
        review.restaurant_id = id
        review.user_id = userId
        # review.posted = datetime.utcnow
        db.session.add(review)
        db.session.commit()
        review = Review.query.filter_by(user_id=userId,restaurant_id=id).order_by(Review.id.desc()).first()
        result = review_schema.dump(review).data
        return { "status": 'success', 'data': result }, 201
    
class ReviewCategory(Resource):        
    @login_required
    def put(self,r_id,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = review_schema.load(json_data)
        if errors:
            return errors, 422
        review = Review.query.filter_by(restaurant_id=r_id,id=id).first()
        # print(review)
        if not review:           
            return {'message': 'review does not exists in that restaurant'}, 400
        userId = GetUserId.user_creds(self)
        response = Review.query.filter_by(user_id=userId,restaurant_id=id,id=id).first()
        if not response:
            return {'message': 'user can only edit reviews they made'}, 401
        review.review=data['review']
        review.rating=data['rating']
        review.restaurant_id=data['restaurant_id']
        review.restaurant_id= r_id
        review.user_id=data['user_id']
        review.user_id = userId
        review.posted = datetime.utcnow()
        db.session.commit()
        # restaurants = Restaurant.query.filter_by(id=id).first()
        result = review_schema.dump(review).data
        print(result)
        if result:
            return {
                "status" : 'success',
                'data' : result,
            }, 200
        
    @login_required
    def delete(self,r_id,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = review_schema.load(json_data)
        if errors:
            return errors, 422
        review = Review.query.filter_by(restaurant_id=id).first()
        # print(review)
        if not review:           
            return {'message': 'review does not exists in that restaurant'}, 400
        
        userId = GetUserId.user_creds(self)
        response = Review.query.filter_by(user_id=userId,restaurant_id=id,id=id).first()
        if not response:
            return {'message': 'user can only edit reviews they made'}, 401
        
        review = Review.query.filter_by(user_id=userId,restaurant_id=id,id=id).delete()
        db.session.commit()

        result = review_schema.dump(review).data

        return { "status": 'success', 'data': result}, 204
    
class InformationResource(Resource):
    @login_required
    def get(self,id):
        information = Information.query.filter_by(restaurant_id=id).all()
        informations = informations_schema.dump(information).data
        if informations:
            return {
                'status': 'success',
                'data': informations
            }, 200
        return {
            'status': 'No informations found for that restaurant',
        }, 400
    
    @login_required
    def post(self,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = information_schema.load(json_data)
        if errors:
            return errors, 422
        information = Information.query.filter_by(restaurant_id=id).first()
        # print(information)
        if information:           
            return {'message': 'information already exists in that restaurant'}, 400
        information = Information(
            timeOpen=json_data['timeOpen'],
            timeClosed=json_data['timeClosed'],
            location=json_data['location'],
            contact=json_data['contact'],
            description=json_data['description'],
            restaurant_id=id
            )
        print(information.restaurant_id)
        information.restaurant_id = id
        db.session.add(information)
        db.session.commit()
        result = information_schema.dump(information).data
        return { "status": 'success', 'data': result }, 201
           
    @login_required
    def put(self,id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = information_schema.load(json_data)
        if errors:
            return errors, 422
        information = Information.query.filter_by(restaurant_id=id).first()
        # print(information)
        if not information:           
            return {'message': 'information does not exists in that restaurant'}, 400
        
        information.timeOpen=data['timeOpen']
        information.timeClosed=data['timeClosed']
        information.location=data['location']
        information.contact=data['contact']
        information.description=data['description']
        information.restaurant_id=data['restaurant_id']
        information.restaurant_id= id
        db.session.commit()
        # restaurants = Restaurant.query.filter_by(id=id).first()
        result = information_schema.dump(information).data
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
        data, errors = information_schema.load(json_data)
        if errors:
            return errors, 422
        information = Information.query.filter_by(restaurant_id=id).first()
        # print(information)
        if not information:           
            return {'message': 'information does not exists in that restaurant'}, 400
        information = Information.query.filter_by(restaurant_id=id).delete()
        db.session.commit()

        result = information_schema.dump(information).data

        return { "status": 'success', 'data': result}, 204
    
class OrderResource(Resource):
    @login_required
    def get(self,id):
        order = Order.query.filter_by(restaurant_id=id).all()
        orders = orders_schema.dump(order).data
        if orders:
            return {
                'status': 'success',
                'data': orders
            }, 200
        return {
            'status': 'No orders found for that restaurant',
        }, 400
       
class UserOrder(Resource):
    @login_required 
    def post(self,id,f_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = order_schema.load(json_data)
        if errors:
            return errors, 422
        order = Order(
            timeOrdered=json_data['timeOrdered'],
            food_id=json_data['food_id'],
            price=json_data['price'],
            user_id=json_data['user_id'],
            restaurant_id=id
            )
        order.restaurant_id = id
        userId = GetUserId.user_creds(self)
        order.user_id = userId
        order.food_id = f_id
        db.session.add(order)
        db.session.commit()
        result = order_schema.dump(order).data
        return { "status": 'success', 'data': result }, 201
   
class OrderRetrieve(Resource):        
    @login_required
    def put(self,id,r_id,f_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = order_schema.load(json_data)
        if errors:
            return errors, 422
        order = Order.query.filter_by(id=id).first()
        # print(order)
        if not order:           
            return {'message': 'Order doesn\'t exists'}, 400
        userId = GetUserId.user_creds(self)
        order = Order.query.filter_by(id=id,user_id=userId).first()
        # print(order)
        if not order:           
            return {'message': 'user can only edit reviews they made'}, 400
        
        order.timeOrdered=data['timeOrdered']
        order.food_id=data['food_id']
        order.price=data['price']
        order.user_id=data['user_id']
        order.restaurant_id=data['restaurant_id']
        order.food_id= f_id
        order.user_id= userId
        order.restaurant_id= r_id
        db.session.commit()
        result = order_schema.dump(order).data
        print(result)
        if result:
            return {
                "status" : 'success',
                'data' : result,
            }, 200
        
    @login_required
    def delete(self,id,r_id,f_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = order_schema.load(json_data)
        if errors:
            return errors, 422
        order = Order.query.filter_by(id=id).first()
        # print(order)
        if not order:           
            return {'message': 'Order doesn\'t exists'}, 400
        userId = GetUserId.user_creds(self)
        order = Order.query.filter_by(id=id,user_id=userId).first()
        # print(order)
        if not order:           
            return {'message': 'user can only edit reviews they made'}, 400
        order = Order.query.filter_by(id=id).delete()
        db.session.commit()

        result = order_schema.dump(order).data

        return { "status": 'success', 'data': result}, 204