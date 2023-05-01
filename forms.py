# This file contains forms that your users can fill out and submit data to your Flask app.
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, FloatField, HiddenField
from wtforms.validators import DataRequired, Email, Length
from models import FishingLocation

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()

class FishingLocationForm(FlaskForm):
    name = StringField('Name', validators= [DataRequired(), Length(min=1, max=50)])
    description = TextAreaField('Description', validators=[DataRequired()])
    google_map_pin = StringField('Google Map Pin', validators=[DataRequired()])
    latitude = HiddenField('Latitude', validators=[DataRequired()])
    longitude = HiddenField('Longitude', validators=[DataRequired()])
    submit_button = SubmitField()