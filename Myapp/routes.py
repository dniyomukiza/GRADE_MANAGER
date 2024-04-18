from flask import Blueprint, redirect, url_for, render_template

from .extensions import db
from .models import User

main = Blueprint('main', __name__, template_folder='templates')


# Landing page route
@main.route('/')
def landing_page():
    return render_template('landing_page.html')


# Login route
@main.route('/login')
def login():
    # Add login functionality here
    return "Login Page"  # For demonstration purposes, just return a string


# Register route
@main.route('/register')
def register():
    # Add register functionality here
    return "Register Page"  # For demonstration purposes, just return a string
