from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Initialize Bootstrap extension for easy form rendering
    Bootstrap5(app)

    # Initialize Bcrypt for secure password hashing
    Bcrypt(app)

    # Configure a secret key for session management (Consider using an environment variable)
    app.secret_key = 'somerandomvalue'

    # Configure and initialize the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

    # Configure the upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

    # Initialize the Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Create a user loader function that takes a user_id and returns a User object
    from .models import User  # Importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints for various components
    from . import views
    app.register_blueprint(views.mainbp)

    from . import destinations
    app.register_blueprint(destinations.destbp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    from . import api
    app.register_blueprint(api.api_bp)

    # Error handler for 404 errors
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", error=e)

    # Create a context processor to provide variables to all templates
    @app.context_processor
    def get_context():
        year = datetime.datetime.today().year
        return dict(year=year)

    return app
