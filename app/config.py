from flask import Flask, request, jsonify, render_template, redirect, url_for, session, make_response
import datetime
from app.models import Application, ApplicationList
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize ApplicationList
application_list = ApplicationList()
application_list.initialize()
