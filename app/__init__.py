import webbrowser

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask import session

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def page_not_found(e):
    return render_template('Error404.html', title="Error 404"), 404


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Nashonsapp'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

    db.init_app(app)

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_error_handler(404, page_not_found)
    # webbrowser.open('http://127.0.0.1:5000/')
    return app
