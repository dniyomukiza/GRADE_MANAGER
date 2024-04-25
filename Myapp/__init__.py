import os
from flask import Flask
from flask_login import LoginManager
from .extensions import db
from .models import User
from .routes import main, login

os.environ["DATABASE_URL"] = ("postgresql://capstone_db_n1ya_user:zHsZR3l94vYHIINd5KncUu0VYJVamBBj@dpg"
                              "-cogk57vsc6pc73d6ho5g-a.oregon-postgres.render.com/capstone_db_n1ya")

login_manager = LoginManager()

login_manager.login_view = 'login.html'  # Set the login view for unauthorized users


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)

    login_manager.init_app(app)

    app.secret_key = 'This is for Cross-Site Request Forgery protection'

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    db.init_app(app)

    app.register_blueprint(main)
    return app
