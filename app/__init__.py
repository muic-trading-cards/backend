from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.shared import *
from app.schema import *

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
    app.config['SECRET_KEY'] = 'thisisasecret'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .schema import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        s = Session()
        user = s.query(User).get(int(user_id))
        s.close()
        return user

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for listing parts of app
    from .listing import listing as listing_blueprint
    app.register_blueprint(listing_blueprint)

    # blueprint for listing parts of app
    from .card import card as card_blueprint
    app.register_blueprint(card_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app