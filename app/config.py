from flask import Flask, request, jsonify, render_template, redirect, url_for, session, make_response, flash, g
import datetime
from app.models import Application, db, bcrypt, User, Company, StatusChange
from dotenv import load_dotenv
from app.utils import login_required
from sqlalchemy import func

# Load environment variables
load_dotenv()

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:flaskpass@localhost:3307/applications_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Initialize Bcrypt
bcrypt.init_app(app)

with app.app_context():
    db.create_all()  # Create tables if they don't exist

