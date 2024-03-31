from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

# create SQL-Alchemy instance
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # bind SQLAlchemy with flask app
    db.init_app(app)

    # Import views and authentication blueprints
    from .views import views
    from .auth import auth

    # register blueprint for routing
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models to create database tables
    from .models import User, File

    # create database with tables defined in models.py
    with app.app_context():
        db.create_all()

    # logic for authentication
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # callback function that loads user object based on ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # return configured Flask app
    return app
