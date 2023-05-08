from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db as root_db, login_manager, ma
from helpers import JSONEncoder
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "https://scoutfortrout.com"]},
                     r"/signup": {"origins": ["http://localhost:5173", "https://scoutfortrout.com"]}})

# google maps
# app.config['GOOGLE_MAPS_API_KEY'] = os.getenv('GOOGLE_MAPS_API_KEY')

# routes
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
app.json_encoder = JSONEncoder
app.config.from_object(Config)

# database
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)

# create database tables
with app.app_context():
    # code that requires application context
    root_db.create_all()
