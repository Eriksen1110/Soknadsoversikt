from flask import Flask, request, jsonify, render_template, redirect, url_for, session, make_response, flash, g
import datetime
from models import Application, db, bcrypt, User, Company, StatusChange
from dotenv import load_dotenv
from utils import login_required
from sqlalchemy import func
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY') 

MODE = os.getenv('MODE', 'development')
if MODE == 'production':
    app.config['DEBUG'] = False
else:
    app.config['DEBUG'] = True

PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', 'localhost')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MY_SQL_USER')}:{os.getenv('MY_SQL_PASSWORD')}@{os.getenv('MY_SQL_URL')}/applications_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Initialize Bcrypt
bcrypt.init_app(app)

with app.app_context():
    db.create_all()  # Create tables if they don't exist

