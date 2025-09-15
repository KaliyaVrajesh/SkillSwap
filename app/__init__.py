from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    moment.init_app(app)

    # Flask-Login settings
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Import models
    from app import models

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    # Register blueprints
    from app.routes import main_bp, auth_bp, profile_bp, swaps_bp
    from app.admin import admin_bp  # ADD THIS LINE
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(swaps_bp)
    app.register_blueprint(admin_bp)  # ADD THIS LINE

    # Create database tables before first request
    @app.before_request
    def create_tables():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database creation failed: {e}")
            # Continue anyway - tables might already exist

    return app
    app = create_app()
