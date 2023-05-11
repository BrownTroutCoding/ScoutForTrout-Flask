# The models page is used for creating classes that we'll use repeatedly to populate our databases.
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
# db represents the database
db = SQLAlchemy()

# Function that Flask-Login will use to load the current user. It takes in the user ID and returns
#  the corresponding User object.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Defines the database schema for the 'users' table. id is the primary key

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, g_auth_verify=False):
        self.id = self.set_id()
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f'User {self.email} has been added to the database'



    
class FishingLocation(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.Text)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, id, name, latitude, longitude, description, user_id):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return f'The following fishing location has been added to the inventory: {self.name}.'

class FishingLocationSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'latitude', 'longitude', 'description', 'user_id']

fishing_location_schema = FishingLocationSchema()
all_locations_schema = FishingLocationSchema(many=True)

# class GoogleMapPin(db.Model):
#     id = db.Column(db.String, primary_key=True)
#     user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)
#     fishing_location_id = db.Column(db.Integer, db.ForeignKey('fishing_location.id'), nullable=False)
#     latitude = db.Column(db.Float, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)

#     user = db.relationship('User', backref='google_map_pins')
#     fishing_location = db.relationship('FishingLocation', backref='pins')

# class GoogleMapPinSchema(ma.Schema):
#     class Meta:
#         fields = ['id', 'user_id', 'fishing_location_id', 'latitude', 'longitude']

# google_map_pin_schema = GoogleMapPinSchema()
# google_map_pins_schema = GoogleMapPinSchema(many=True)

# class RiverData(db.Model):
#     __tablename__ = 'river_data'
#     id = db.Column(db.String, primary_key=True)
#     river = db.Column(db.String, nullable=False)
#     date = db.Column(db.DateTime, nullable=False)
#     value = db.Column(db.Float, nullable=False)
#     data_type = db.Column(db.String, nullable=False)
    
# class RiverCondition(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     fishing_location_id = db.Column(db.Integer, db.ForeignKey('fishing_location.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     water_cfs = db.Column(db.Integer, nullable=False)
#     water_temperature = db.Column(db.Float, nullable=False)
#     water_clarity = db.Column(db.Float, nullable=False)
#     fishing_location = db.relationship('FishingLocation', backref='river_condition')

# class RiverConditionSchema(ma.Schema):
#     class Meta:
#         fields = ['id', 'fishing_location_id', 'date', 'water_cfs', 'water_temperature', 'water_clarity']

# river_condition_schema = RiverConditionSchema()
# river_conditions_schema = RiverConditionSchema(many=True)

# class WeatherForecast(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     fishing_location_id = db.Column(db.Integer, db.ForeignKey('fishing_location.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     high_temp = db.Column(db.Float, nullable=False)
#     low_temp = db.Column(db.Float, nullable=False)
#     wind_speed = db.Column(db.Float, nullable=False)
#     precipitation_type = db.Column(db.Float, nullable=False)
#     precipitation_chance = db.Column(db.Float, nullable=False)
#     cloud_cover = db.Column(db.Float, nullable=False)

#     fishing_location = db.relationship('FishingLocation', backref='weather_forecast')

# class WeatherForecastSchema(ma.Schema):
#     class Meta:
#         fields = ['id', 'fishing_location_id', 'date', 'high_temp', 'low_temp', 'wind_speed', 'precipitation_type', 'precipitation_chance', 'cloud_cover']

# weather_forecast_schema = WeatherForecastSchema()
# weather_forecasts_schema = WeatherForecastSchema(many=True)

# class FlyRecommendation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     fishing_location_id = db.Column(db.Integer, db.ForeignKey('fishing_location.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     fly_type = db.Column(db.String(50), nullable=False)
#     fly_pattern = db.Column(db.Text, nullable=False)
#     hatch = db.Column(db.Text, nullable=False)

#     fishing_location = db.relationship('FishingLocation', backref='fly_recommendation')

# class FlyRecommendationSchema(ma.Schema):
#     class Meta:
#         fields = ['id', 'fishing_location_id', 'date', 'fly_type', 'fly_pattern', 'hatch']

# fly_recommendation_schema = FlyRecommendationSchema()
# fly_recommendations_schema = FlyRecommendationSchema(many=True)