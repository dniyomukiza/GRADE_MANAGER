import os
from flask import Flask
from .extensions import db
from .routes import main

os.environ["DATABASE_URL"] = ("postgresql://capstone_db_n1ya_user:zHsZR3l94vYHIINd5KncUu0VYJVamBBj@dpg"
                              "-cogk57vsc6pc73d6ho5g-a.oregon-postgres.render.com/capstone_db_n1ya")


def create_app():
    app = Flask(__name__)
    app.secret_key = 'This is for Cross-Site Request Forgery protection'
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")


    db.init_app(app)

    app.register_blueprint(main)

    return app
