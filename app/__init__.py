from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create a single SQLAlchemy instance
db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from app.models import Olympiad

    return Olympiad.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login_organizer"

    # Initialize database
    with app.app_context():
        from app import routes

        routes.init_app(app)  # Register the blueprint

        db.create_all()

    return app
