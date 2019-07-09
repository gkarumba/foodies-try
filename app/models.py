from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow

ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    location = db.Column(db.String(255))
    phonenumber = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(255))     
    review = db.relationship('Review',backref = 'user',lazy = "dynamic")
    order = db.relationship('Order',backref = 'user',lazy = "dynamic")
    
    # def save_comment(self):
    #     db.session.add(self)
    #     db.session.commit()

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        # print(self.password_hash)
        # print(password)
        return check_password_hash(self.password_hash,password)

    def __init__(self, username, email, phonenumber, password_hash, role, location):
        self.username = username
        self.email = email
        self.phonenumber = phonenumber
        self.password_hash = password_hash
        self.location = location
        self.role = role

class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True, validate=validate.Length(1))
    password_hash = fields.String(required=True, validate=validate.Length(1))
    location = fields.String(required=True, validate=validate.Length(1))

class LoginSchema(ma.Schema):
    email = fields.String(required=True, validate=validate.Length(1))
    password_hash = fields.String(required=True, validate=validate.Length(1))

    # def __repr__(self):
    #     return f'User {self.username}'
    
class Restaurant(db.Model):
    
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    # information = db.Column(db.String)
    informations = db.relationship('Information',backref = 'restaurant',lazy = "dynamic")
    review = db.relationship('Review',backref = 'restaurant',lazy = "dynamic")
    
    # def save_restaurant(self):
    #     db.session.add(self)
    #     db.session.commit()
    def __init__(self,name,location,):
        self.name = name
        self.location = location
        
    @classmethod
    def get_restaurants(cls):
        restaurants = Restaurant.query.order_by('id').all()      
        return restaurants
    
    @classmethod
    def get_restaurant(cls,id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        return restaurant 

class RestaurantSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    location = fields.String(required=True, validate=validate.Length(1))
  
class Food(db.Model):
    
    __tablename__ = 'foods'

    id = db.Column(db.Integer,primary_key = True)
    foods= db.Column(db.String)
    category = db.Column(db.String)
    description= db.Column(db.String)
    price = db.Column(db.Integer)
    restaurant_id = db.Column(db.Integer)
    
    def __init__(self,foods,category,description,price,restaurant_id):
        self.foods = foods
        self.category = category
        self.description = description
        self.price = price
        self.restaurant_id = restaurant_id
        

class FoodSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    foods = fields.String(required=True)
    category = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    price = fields.Integer(required=True)
    restaurant_id = fields.Integer(required=True)
    
    
    
class Recipe(db.Model):
    
    __tablename__ = 'recipes'

    id = db.Column(db.Integer,primary_key = True)
    recipe_name = db.Column(db.String)
    food_id= db.Column(db.Integer)
    description= db.Column(db.String)
    restaurant_id = db.Column(db.Integer)
    
    def __init__(self,recipe_name,description,restaurant_id):
        self.recipe_name = recipe_name
        self.description = description
        self.restaurant_id = restaurant_id

    @classmethod
    def get_recipe(cls, id):
        recipe = Recipe.query.filter_by(restaurant_id=id).all()
        return recipe

class RecipeSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    recipe_name = fields.String(required=True)
    description = fields.String(required=True, validate=validate.Length(1))
    # food_id = fields.Integer(required=True, validate=validate.Length(1))
    restaurant_id = fields.Integer(required=True)
    

    
class Review(db.Model):
    
    __tablename__ = 'reviews'

    id = db.Column(db.Integer,primary_key = True)
    review = db.Column(db.String)
    rating = db.Column(db.Integer)
    posted=db.Column(db.DateTime,default=datetime.utcnow)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self,review,rating,restaurant_id,user_id):
        self.review = review
        self.rating = rating
        # self.posted= posted
        self.restaurant_id = restaurant_id
        self.user_id = user_id
        

    @classmethod
    def get_review(cls, id):
        review = Review.query.filter_by(restaurant_id=id).all()
        return review

    @classmethod
    def get_all_reviews(cls):
        reviews = Review.query.order_by('id').all()
        return reviews

class ReviewSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    review = fields.String(required=True)
    rating = fields.Integer(required=True)
    posted = fields.DateTime(required=True)
    restaurant_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)

class Information(db.Model):
    
    __tablename__ = 'informations'

    id = db.Column(db.Integer,primary_key = True)
    timeOpen = db.Column(db.DateTime)
    timeClosed = db.Column(db.DateTime)
    description = db.Column(db.String)
    location = db.Column(db.String)
    contact  =  db.Column(db.String)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    
    def __init__(self,timeOpen,timeClosed,description,location,contact,restaurant_id):
        self.timeOpen = timeOpen
        self.timeClosed = timeClosed
        self.description = description
        self.location = location
        self.contact = contact
        self.restaurant_id = restaurant_id

    @classmethod
    def get_information(cls, id):
        information = Information.query.filter_by(restaurant_id=id).all()
        return information

    @classmethod
    def get_all_informations(cls):
        informations = Information.query.order_by('id').all()
        return informations

class InformationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    timeOpen = fields.String(required=True)
    timeClosed = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    location = fields.String(required=True, validate=validate.Length(1))
    contact = fields.String(required=True, validate=validate.Length(1))
    restaurant_id = fields.Integer(required=True)
 
class Order(db.Model):
    
    __tablename__ = 'orders'

    id = db.Column(db.Integer,primary_key = True)
    timeOrdered = db.Column(db.DateTime,default=datetime.utcnow)
    food_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    restaurant_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,timeOrdered,food_id,price,restaurant_id,user_id):
        self.timeOrdered = timeOrdered
        self.food_id = food_id
        self.price = price
        self.restaurant_id = restaurant_id
        self.user_id = user_id     
    
    @classmethod
    def get_order(cls, id):
        order = Order.query.filter_by(restaurant_id=id).all()
        return order

class OrderSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    timeOrdered = fields.String(required=True)
    food_id = fields.Integer(required=True, validate=validate.Length(1))
    price = fields.Integer(required=True, validate=validate.Length(1))
    user_id = fields.Integer(required=True, validate=validate.Length(1)) 
    restaurant_id = fields.Integer(required=True, validate=validate.Length(1))   
    